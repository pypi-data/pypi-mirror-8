""":mod:`geofrontcli.cli` --- CLI main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from __future__ import print_function

import argparse
import os.path
import subprocess
import sys
import webbrowser

from dirspec.basedir import load_config_paths, save_config_path
from six.moves import input

from .client import (REMOTE_PATTERN, Client, ExpiredTokenIdError,
                     NoTokenIdError, ProtocolVersionError, RemoteError,
                     TokenIdError, UnfinishedAuthenticationError)
from .key import PublicKey
from .version import VERSION


CONFIG_RESOURCE = 'geofront-cli'
SERVER_CONFIG_FILENAME = 'server'

SSH_PROGRAM = None
try:
    SSH_PROGRAM = subprocess.check_output(['which', 'ssh']).strip() or None
except subprocess.CalledProcessError:
    pass

SCP_PROGRAM = None
try:
    SCP_PROGRAM = subprocess.check_output(['which', 'scp']).strip() or None
except subprocess.CalledProcessError:
    pass


parser = argparse.ArgumentParser(description='Geofront client utility')
parser.add_argument(
    '-S', '--ssh',
    default=SSH_PROGRAM,
    required=not SSH_PROGRAM,
    help='ssh client to use' + (' [%(default)s]' if SSH_PROGRAM else '')
)
parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s ' + VERSION)
subparsers = parser.add_subparsers()


def get_server_url():
    for path in load_config_paths(CONFIG_RESOURCE):
        path = os.path.join(path.decode(), SERVER_CONFIG_FILENAME)
        if os.path.isfile(path):
            with open(path) as f:
                return f.read().strip()
    parser.exit('Geofront server URL is not configured yet.\n'
                'Try `{0} start` command.'.format(parser.prog))


def get_client():
    server_url = get_server_url()
    return Client(server_url)


def subparser(function):
    """Register a subparser function."""
    p = subparsers.add_parser(function.__name__, description=function.__doc__)
    p.set_defaults(function=function)
    p.call = function
    return p


@subparser
def start(args):
    """Set up the Geofront server URL."""
    for path in load_config_paths(CONFIG_RESOURCE):
        path = os.path.join(path.decode(), SERVER_CONFIG_FILENAME)
        if os.path.isfile(path):
            message = 'Geofront server URL is already configured: ' + path
            if args.force:
                print(message + '; overwriting...', file=sys.stderr)
            else:
                parser.exit(message)
    while True:
        server_url = input('Geofront server URL: ')
        if not server_url.startswith(('https://', 'http://')):
            print(server_url, 'is not a valid url.')
            continue
        elif not server_url.startswith('https://'):
            cont = input('It is not a secure URL. '
                         'https:// is preferred over http://. '
                         'Continue (y/N)? ')
            if cont.strip().lower() != 'y':
                continue
        break
    server_config_filename = os.path.join(
        save_config_path(CONFIG_RESOURCE).decode(),
        SERVER_CONFIG_FILENAME
    )
    with open(server_config_filename, 'w') as f:
        print(server_url, file=f)
    authenticate.call(args)


start.add_argument('-f', '--force',
                   action='store_true',
                   help='overwrite the server url configuration')


@subparser
def authenticate(args):
    """Authenticate to Geofront server."""
    client = get_client()
    while True:
        with client.authenticate() as url:
            if args.open_browser:
                print('Continue to authenticate in your web browser...')
                webbrowser.open(url)
            else:
                print('Continue to authenticate in your web browser:')
                print(url)
        input('Press return to continue')
        try:
            client.identity
        except UnfinishedAuthenticationError as e:
            print(str(e))
        else:
            break
    home = os.path.expanduser('~')
    ssh_dir = os.path.join(home, '.ssh')
    if os.path.isdir(ssh_dir):
        for name in 'id_rsa.pub', 'id_dsa.pub':
            pubkey_path = os.path.join(ssh_dir, name)
            if os.path.isfile(pubkey_path):
                with open(pubkey_path) as f:
                    public_key = PublicKey.parse_line(f.read())
                    break
        else:
            public_key = None
        if public_key and public_key.fingerprint not in client.public_keys:
            print('You have a public key ({0}), and it is not registered '
                  'to the Geofront server ({1}).'.format(pubkey_path,
                                                         client.server_url))
            while True:
                register = input('Would you register the public key to '
                                 'the Geofront server (Y/n)? ').strip()
                if register.lower() in ('', 'y', 'n'):
                    break
                print('{0!r} is an invalid answer.'.format(register))
            if register.lower() != 'n':
                try:
                    client.public_keys[public_key.fingerprint] = public_key
                except ValueError as e:
                    print(e, file=sys.stderr)
                    if args.debug:
                        raise


@subparser
def keys(args):
    """List registered public keys."""
    client = get_client()
    for fingerprint, key in client.public_keys.items():
        if args.fingerprint:
            print(fingerprint)
        else:
            print(key)


keys.add_argument(
    '-v', '--verbose',
    dest='fingerprint',
    action='store_false',
    help='print public keys with OpenSSH authorized_keys format instead of '
         'fingerprints'
)


@subparser
def masterkey(args):
    """Show the current master key."""
    client = get_client()
    master_key = client.master_key
    if args.fingerprint:
        print(master_key.fingerprint)
    else:
        print(master_key)


masterkey.add_argument(
    '-v', '--verbose',
    dest='fingerprint',
    action='store_false',
    help='print the master key with OpenSSH authorized_keys format instead of '
         'its fingerprint'
)


@subparser
def remotes(args):
    """List available remotes."""
    client = get_client()
    remotes = client.remotes
    if args.alias:
        for alias in remotes:
            print(alias)
    else:
        for alias, remote in remotes.items():
            print('{0}\t{1}'.format(alias, remote))


remotes.add_argument(
    '-v', '--verbose',
    dest='alias',
    action='store_false',
    help='print remote aliases with their actual addresses, not only aliases'
)


@subparser
def authorize(args):
    """Temporarily authorize you to access the given remote.
    A made authorization keeps alive in a minute, and then will be expired.

    """
    client = get_client()
    try:
        client.authorize(args.remote)
    except RemoteError as e:
        print(e, file=sys.stderr)
        if args.debug:
            raise


authorize.add_argument(
    'remote',
    help='the remote alias to authorize you to access'
)


def get_ssh_options(remote):
    """Translate the given ``remote`` to a corresponding :program:`ssh`
    options.  For example, it returns the following list for ``'user@host'``::

        ['-l', 'user', 'host']

    The remote can contain the port number or omit the user login as well
    e.g. ``'host:22'``::

        ['-p', '22', 'host']

    """
    remote_match = REMOTE_PATTERN.match(remote)
    if not remote_match:
        raise ValueError('invalid remote format: ' + str(remote))
    options = []
    user = remote_match.group('user')
    if user:
        options.extend(['-l', user])
    port = remote_match.group('port')
    if port:
        options.extend(['-p', port])
    options.append(remote_match.group('host'))
    return options


@subparser
def colonize(args):
    """Make the given remote to allow the current master key.
    It is equivalent to ``geofront-cli masterkey -v > /tmp/master_id_rsa &&
    ssh-copy-id -i /tmp/master_id_rsa REMOTE``.

    """
    client = get_client()
    remote = client.remotes.get(args.remote, args.remote)
    try:
        options = get_ssh_options(remote)
    except ValueError as e:
        colonize.error(str(e))
    cmd = [args.ssh]
    if args.identity_file:
        cmd.extend(['-i', args.identity_file])
    cmd.extend(options)
    cmd.extend([
        'mkdir', '~/.ssh', '&>', '/dev/null', '||', 'true', ';',
        'echo', repr(str(client.master_key)),
        '>>', '~/.ssh/authorized_keys'
    ])
    subprocess.call(cmd)


colonize.add_argument(
    '-i',
    dest='identity_file',
    help='identity file to use.  it will be forwarded to the same option '
         'of the ssh program if used'
)
colonize.add_argument('remote', help='the remote alias to colonize')


@subparser
def ssh(args):
    """SSH to the remote through Geofront's temporary authorization."""
    while True:
        client = get_client()
        try:
            remote = client.authorize(args.remote)
        except RemoteError as e:
            ssh.error(str(e))
            if args.debug:
                raise
        except TokenIdError:
            print('Authentication required.')
            authenticate.call(args)
        else:
            break
    try:
        options = get_ssh_options(remote)
    except ValueError as e:
        ssh.error(str(e))
    subprocess.call([args.ssh] + options)


ssh.add_argument('remote', help='the remote alias to ssh')


def parse_scp_path(path, args):
    """Parse remote:path format."""
    if ':' not in path:
        return None, None, path
    alias, path = path.split(':', 1)
    while True:
        client = get_client()
        try:
            remote = client.authorize(alias)
        except RemoteError as e:
            print(e, file=sys.stderr)
            if args.debug:
                raise
            raise SystemExit(1)
        except TokenIdError:
            print('Authentication required.')
            authenticate.call(args)
        else:
            break
    return client, remote, path


@subparser
def scp(args):
    options = []
    src_client, src_remote, src_path = parse_scp_path(args.source, args)
    dst_client, dst_remote, dst_path = parse_scp_path(args.destination, args)
    if src_client and dst_client:
        scp.error('source and destination cannot be both '
                  'remote paths at a time')
    elif not (src_client or dst_client):
        scp.error('one of source and destination has to be a remote path')
    if args.ssh:
        options.extend(['-S', args.ssh])
    if args.recursive:
        options.append('-r')
    remote = src_remote or dst_remote
    remote_match = REMOTE_PATTERN.match(remote)
    if not remote_match:
        raise ValueError('invalid remote format: ' + str(remote))
    port = remote_match.group('port')
    if port:
        options.extend(['-P', port])
    host = remote_match.group('host')
    user = remote_match.group('user')
    if user:
        host = user + '@' + host
    if src_remote:
        options.append(host + ':' + src_path)
    else:
        options.append(src_path)
    if dst_remote:
        options.append(host + ':' + dst_path)
    else:
        options.append(dst_path)
    subprocess.call([args.scp] + options)


scp.add_argument(
    '--scp',
    default=SCP_PROGRAM,
    required=not SCP_PROGRAM,
    help='scp client to use' + (' [%(default)s]' if SCP_PROGRAM else '')
)
scp.add_argument(
    '-r', '-R', '--recursive',
    action='store_true',
    help='recursively copy entire directories'
)
scp.add_argument('source', help='the source path to copy')
scp.add_argument('destination', help='the destination path')


for p in authenticate, start, ssh, scp:
    p.add_argument(
        '-O', '--no-open-browser',
        dest='open_browser',
        action='store_false',
        help='do not open the authentication web page using browser.  '
             'instead print the url to open'
    )


def main(args=None):
    args = parser.parse_args(args)
    if getattr(args, 'function', None):
        try:
            args.function(args)
        except NoTokenIdError:
            parser.exit('Not authenticated yet.\n'
                        'Try `{0} authenticate` command.'.format(parser.prog))
        except ExpiredTokenIdError:
            parser.exit('Authentication renewal required.\n'
                        'Try `{0} authenticate` command.'.format(parser.prog))
        except ProtocolVersionError as e:
            parser.exit('geofront-cli seems incompatible with the server.\n'
                        'Try `pip install --upgrade geofront-cli` command.\n'
                        'The server version is {0}.'.format(e.server_version))
    else:
        parser.print_usage()
