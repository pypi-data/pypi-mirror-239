import os
import sys

aurapy_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(aurapy_path)
import aurapy
import aurapy.connection
from . import console
from . import flashage
import argparse
import textwrap


update_source_help = \
"""Firmware update source
can be:
    - 'packaged' (default)
    - 'bundled' (uses binary already present on the board)
    - a path to an *.update file to install or a directory to search for *.update files
"""

update_filter__help = \
"""Update embedded aura software. 
Takes as argument a version specification in the form:
    0.1.2   -> exact match,
    >=0.1.1 -> any version higher than 0.1.1,
    <1.2.1  -> any version strictly lower than 1.2.1.  
If no argument is provided look for available versions strictly higher than the current actuator version.
See also: --path and --gw options
"""

python_exe = os.path.basename(sys.executable)

parser = argparse.ArgumentParser(
    prog=f'{python_exe} -m aurapy',
    description="aurapy options",
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-u", "--update",
                    action="store_true",
                    help="Update embedded aura software")

parser.add_argument("--update-bl",
                    action="store_true",
                    help="Update the aura bootloader")

parser.add_argument("--gw",
                    action='store_true',
                    help="""Apply update(s) to the aura Gateway instead of the actuator 
                            (either --update or --update-bl)""")

parser.add_argument("--update-filter",
                    nargs='?',
                    default=flashage.NO_VERSION_FILTER,
                    help=textwrap.dedent(update_filter__help))

parser.add_argument("--update-source",
                    nargs='?',
                    default=None,
                    const=flashage.PACKAGED_BINARIES,
                    help=textwrap.dedent(update_source_help))

parser.add_argument("-c", "--command",
                    help="console commands",
                    type=str,
                    default=None)

parser.add_argument("--no-prompt",
                    action='store_true',
                    help="""Turn off prompt for manual validation during firmware update process.""")

parser.add_argument("-m", "--mock-ports", nargs='*',
                    help=textwrap.dedent(f"""
                    Simulate connected actuators on mock ports.
                        usage: 
                            {aurapy._aura_pybind.mock_group_syntax}
                        
                        example: 
                            {aurapy._aura_pybind.mock_group_example}                            
                    """))

parser.add_argument("--list-ports",
                    action='store_true',
                    help="""lists available serial ports""")

parser.add_argument("-v", "--version",
                    action='store_true',
                    help="print version")

args = parser.parse_args()


def main_func(args):
    if args.version:
        print(aurapy.get_version())

    if args.mock_ports is not None:
        if not args.mock_ports:
            args.mock_ports = ['']

        for port in args.mock_ports:
            try:
                aurapy._aura_pybind.register_mock_device(port)
            except Exception as exc:
                print("Invalid mock port specification:", aurapy.format_cpp_error_message(str(exc)))
                return

    if args.list_ports is not None:
        for port in aurapy.connection.available_ports():
            aurapy.connection.print_port(port)
            print()

    try:
        if args.update or args.update_bl or args.update_source is not None:

            if args.gw:
                func = flashage.connect_and_update_aura_gw
            else:
                func = flashage.connect_and_update_aura

            func(version_filter=args.update_filter,
                 update_source=args.update_source if args.update_source is not None else flashage.PACKAGED_BINARIES,
                 interactive=not args.no_prompt,
                 update_app=args.update,
                 update_bootloader=args.update_bl)

        elif (not args.list_ports and not args.version) or args.command:
            # do not run the console if asking to list ports or version
            console.run_console_loop(initial_command=args.command,
                                     no_loop=args.command is not None)

    except Exception as exc:
        print(str(exc))
        sys.exit(1)

    aurapy._aura_pybind.clear_mock_devices()


main_func(args)
