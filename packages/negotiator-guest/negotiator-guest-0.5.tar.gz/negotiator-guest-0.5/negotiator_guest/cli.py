# Generic QEMU guest agent in Python.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: September 24, 2014
# URL: https://negotiator.readthedocs.org

"""
Usage: negotiator-guest [OPTIONS]

Start the negotiator-guest daemon.

Supported options:

  -l, --list-commands

    List the commands that the host exposes to its guests.

  -e, --execute=COMMAND

    Execute the given command on the KVM/QEMU host. The standard output stream
    of the command on the host is intercepted and copied to the standard output
    stream on the guest. If the command exits with a nonzero status code the
    negotiator-guest program will also exit with a nonzero status code.

  -d, --daemon

    Start the guest daemon. When using this command line option the
    `negotiator-guest' program never returns (unless an unexpected error
    condition occurs).

  -c, --character-device=PATH

    By default the appropriate character device is automatically selected based
    on /sys/class/virtio-ports/*/name. If the automatic selection doesn't work,
    you can set the absolute pathname of the character device that's used to
    communicate with the negotiator-host daemon running on the KVM/QEMU host.

  -v, --verbose

    Make more noise (enables debugging).

  -q, --quiet

    Only show warnings and errors.

  -h, --help

    Show this message and exit.
"""

# Standard library modules.
import getopt
import logging
import shlex
import sys

# External dependencies.
import coloredlogs

# Modules included in our project.
from negotiator_common.config import GUEST_TO_HOST_CHANNEL_NAME, HOST_TO_GUEST_CHANNEL_NAME
from negotiator_guest import GuestAgent, find_character_device

# Initialize a logger for this module.
logger = logging.getLogger(__name__)


def main():
    """Command line interface for the ``negotiator-guest`` program."""
    # Initialize logging to the terminal.
    coloredlogs.install(level=logging.INFO)
    # Parse the command line arguments.
    list_commands = False
    execute_command = None
    start_daemon = False
    character_device = None
    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'le:dc:vqh', [
            'list-commands', 'execute=', 'daemon', 'character-device=',
            'verbose', 'quiet', 'help'
        ])
        for option, value in options:
            if option in ('-l', '--list-commands'):
                list_commands = True
            elif option in ('-e', '--execute'):
                execute_command = value
            elif option in ('-d', '--daemon'):
                start_daemon = True
            elif option in ('-c', '--character-device'):
                character_device = value
            elif option in ('-v', '--verbose'):
                coloredlogs.increase_verbosity()
            elif option in ('-q', '--quiet'):
                coloredlogs.decrease_verbosity()
            elif option in ('-h', '--help'):
                usage()
                sys.exit(0)
        if not (list_commands or execute_command or start_daemon):
            usage()
            sys.exit(0)
    except Exception:
        logger.exception("Failed to parse command line arguments!")
        sys.exit(1)
    # Start the guest daemon.
    try:
        if not character_device:
            channel_name = HOST_TO_GUEST_CHANNEL_NAME if start_daemon else GUEST_TO_HOST_CHANNEL_NAME
            character_device = find_character_device(channel_name)
        ga = GuestAgent(character_device)
        if start_daemon:
            ga.enter_main_loop()
        elif list_commands:
            print('\n'.join(ga.call_remote_method('list_commands')))
        elif execute_command:
            output = ga.call_remote_method('execute', *shlex.split(execute_command), capture=True)
            print(output.rstrip())
    except Exception:
        logger.exception("Caught a fatal exception! Terminating ..")
        sys.exit(1)


def usage():
    """Print a user friendly usage message to the terminal."""
    print(__doc__.strip())
