"""
 console: a command-line interface for driving aura actuator.
"""
import os.path

from . import auraclient, flashage
import time
from .units import *
from .connection import IOException, TimeoutException, print_exc
from .dialog_utils import prompt_user_yes_no
import sys


class SelectClientException (Exception):

    def __init__(self, serial_port_name='', aura_id=None):
        super().__init__()
        self.serial_port_name = serial_port_name
        self.aura_id = aura_id


def print_basic_usage():
    print("""Aura command line tool.
    press <CTRL> + C once to stop actuator, twice to exit.
    type help for usage.""")


def print_usage():
    print_basic_usage()
    print("""
sample usage:
    st[o]p        -> stops the actuator
    [st]ate       -> fetches actuator state
    [d]uty 0.2    -> sets pwm to 20%
    [s]peed 100   -> sets speed to 100 rpm
    [s]peed_[pid] -> gets/sets the pid parameters when using speed control
    [p]osition 65 -> sets position target to a 65 degrees angle
    [p]os_[pid]   -> gets/sets the pid parameters when using position control
    [c]urrent 1.5 -> sets current target to 1.5 ampere
    [w]ait 1.5    -> sleeps 1.5 second (useful for chaining commands)
    reboot        -> reboot the actuator
    [sel]ect      -> in the case several actuators are connected, selects a different one.   
    version       -> shows client and actuator version
    update        -> updates the actuator firmware
    save          -> persists any temporary changes to the actuator configuration
    [h]elp        -> prints usage

* Numerical parameters support range syntax: start:end:increment:wait_time
    example: 
        speed 100:300:10:0.5 # sets speed from 100 to 300 rpm in increments of 10rpm every 0.5 seconds 
        
* update command can take a filter to match a specified version, (you can use >,<=,=,...)
         and an optional file path
    example:
        update 1.*.* # only search for updates matching 1.*.*
        
* Chain command using ';' as a separator e.g.: speed 100; wait 1; speed 300    
* Press <enter> to repeat the previous command.

Any invalid command will stop the actuator.
    """)


class InvalidCommand(Exception):
    pass


def validate_num_args(command, expected_num_args, *args):
    if len(args) != expected_num_args:
        raise InvalidCommand(f"{command} expects {expected_num_args} arg(s) but got {len(args)}: {' '.join(args)}")


def print_answer(*args):
    print('\t\t', ' '.join([str(arg) for arg in args]).replace('\n', '\n\t\t'))


def parse_float_value(val_str, val_type):
    """
    construct a float-like value from a string.
    :param val_str: a string representing a float.
    :param val_type: type of the float-like value (e.g. units types like ampere, volt, celsius)
    :return: a val_type instance
    """
    return val_type(float(val_str))


def range_gen(start, end, increment):
    """
    a range generator that works with floats too:
    returns values from start to end (exclusive) every increment.

    :param start: start value
    :param end: end value (exclusive)
    :param increment: step between
    :return: a value in [start, end[ of the same type as start.
    """
    val = start
    if start < end:
        while start < end:
            yield val
            val += abs(increment)
    elif start > end:
        while start > end:
            yield val
            val -= abs(increment)
    else:
        # start == end
        yield val


is_verbose = False


def parse_apply(func, val_str, val_type):
    """
    Parses an input to a function and calls the function on that input.
    Note that val_str can specify a range of values in which case
    func will be called repeatedly on those values.

    :param func: function to call
    :param val_str: function input in string format.
    :param val_type: type of the input expected by func
    :return:
    """
    if ':' in val_str:
        vals = val_str.split(':')
        start_str, end_str, increment_str, wait_time_str = vals
        start = parse_float_value(start_str, val_type)
        end = parse_float_value(end_str, val_type)

        increment_tokens = increment_str.split(',')

        increment = parse_float_value(increment_tokens[-1], val_type)
        if len(increment_tokens) > 1:
            pass

        wait_time = float(wait_time_str)

        for val in range_gen(start, end, increment):
            if is_verbose:
                print(func.__name__, val, f'wait {wait_time:.3f}s')

            func(val)
            time.sleep(wait_time)

    else:
        if is_verbose:
            print(func.__name__, val_str)

        func(parse_float_value(val_str, val_type))


def parse_command(client, command, *args):
    """
    Interpret a command string and its arguments to call the
    corresponding method on an AuraClient instance.

    :param client: AuraClient instance to apply the command to
    :param command: a string representing a command line input.
    :param args: optional command arguments as string.
    :return:
    """
    try:
        global is_verbose
        if command == 'verbose':
            validate_num_args(command, 0)
            is_verbose = not is_verbose                
            client._aura_client_impl.set_verbose(is_verbose)

        elif command == 'noverbose':
            validate_num_args(command, 0)
            is_verbose = False

        elif command in ('st', 'state'):
            validate_num_args(command, 0, *args)
            print_answer(client.pull_state())

        elif command in ('s', 'speed'):
            if len(args) > 0:
                validate_num_args(command, 1, *args)
                parse_apply(client.command_speed, args[0], rpm)
            else:
                print_answer(client.pull_state().speed)

        elif command in ('c', 'current'):
            if len(args) > 0:
                validate_num_args(command, 1, *args)
                parse_apply(client.command_current, args[0], ampere)
            else:
                print_answer(client.pull_state().current)

        elif command in ('b', 'brake'):
            if len(args) > 0:
                validate_num_args(command, 1, *args)
                parse_apply(client.command_brake_current, args[0], ampere)
            else:
                print_answer(client.pull_state().current)

        elif command in ('p', 'position'):
            if len(args) > 0:
                validate_num_args(command, 1, *args)
                parse_apply(client.command_position, args[0], degree)
            else:
                print_answer(client.pull_state().position)

        elif command in ('clear_config', ):
            if prompt_user_yes_no("are you sure?", default_yes=False):
                if client._aura_client_impl.clear_configuration():
                    print("configuration cleared")

        elif command in ('t', 'torque'):
            if len(args) > 0:
                validate_num_args(command, 1, *args)
                # TODO: incomplete feature
                parse_apply(client._aura_client_impl.command_torque, args[0], newton_meter)
            else:
                # TODO: return torque, not current
                print_answer(client.pull_state().current)

        elif command in ('d', 'duty'):
            if len(args) > 0:
                validate_num_args(command, 1, *args)
                parse_apply(client.command_dutycycle, args[0], dutycycle)
            else:
                print_answer(client.pull_state().dutycycle)

        elif command in ('o', 'stop'):
            validate_num_args(command, 0)
            if is_verbose:
                print('stop')
            client.stop()

        elif command in ('reboot',):
            if is_verbose:
                print('reboot')
            client.reboot()

        elif command in ('version',):
            validate_num_args(command, 0)
            print_answer('Aura client  :', client.get_client_version())
            print_answer('Aura actuator:', client.get_connected_version())
            aura_hub = client._aura_client_impl.get_aura_hub()
            try:
                if not aura_hub.has_direct_aura_mc_connection():
                    print_answer('Aura gateway :', aura_hub.get_connected_version())
            except:
                # guarding against legacy (pre aura_mc 2.1.5) UTF-8 conversion error when returning non-ascii UUID
                pass

        elif command in ('w', 'wait'):
            validate_num_args(command, 1, *args)
            val = float(args[0])
            if is_verbose:
                print(f"wait {val:.3f}s")
            time.sleep(val)

        elif command in ('calib_icmu',):
            if len(args) == 0:
                client.calibrate_icmu_encoder()
            elif len(args) == 1:
                client.calibrate_icmu_encoder(num_rotations=float(args[0]))
            else:
                validate_num_args(command, 2, *args)
                client.calibrate_icmu_encoder(num_rotations=float(args[0]), debug=bool(args[2]))

        elif command in ('save',):
            validate_num_args(command, 0, *args)
            if client.persist_aura_local_configuration():
                print_answer("Configuration successfully saved")
            else:
                print_answer("An error occurred, the configuration was not saved")

        elif command in ('spid', 'speed_pid'):
            if len(args) > 0:
                validate_num_args(command, 3, *args)
                if not client.push_speed_pid(float(args[0]), float(args[1]), float(args[2])):
                    print_answer("An error occurred")
            else:
                for i in zip(("KP: ", "KI: ", "KD: "), client.pull_speed_pid()):
                    print(*i)

        elif command in ('ppid', 'pos_pid'):
            if len(args) > 0:
                validate_num_args(command, 3, *args)
                if not client.push_position_pid(float(args[0]), float(args[1]), float(args[2])):
                    print_answer("An error occurred")
            else:
                for i in zip(("KP: ", "KI: ", "KD: "), client.pull_position_pid()):
                    print(*i)

        elif command in ('h', 'help', 'doc'):
            validate_num_args(command, 0)
            print_usage()

        elif command in ('update',):
            file_path = None
            version = None
            choose = False

            if len(args) > 0:

                if os.path.exists(args[-1]):
                    file_path = args[-1]
                    args = args[:-1]

                if args:
                    version = ''.join(args)
                    if version.translate({ord(i): None for i in "<>=* .0123456789"}):
                        raise InvalidCommand("""update expects 1 argument representing a filter to apply to the update selection
                     (ex : >0.0.5 | <= 1 | =0.1)""")
                    choose = True

            flashage.update_aura(client,
                                 version_filter=version,
                                 path=file_path,
                                 choose=choose)

        elif command in ('sel', 'select'):
            aura_id = None
            if len(args) > 0:
                validate_num_args(command, 0)
                aura_id = int(args[0])
            raise SelectClientException(serial_port_name=client.get_port_name(), aura_id=aura_id)

        elif command == 'exit':
            validate_num_args(command, 0)
            return True  # exit requested

        elif command.startswith('a'):
            # everything after the '_' is interpreted as an ascii command
            try:
                reply = client._aura_client_impl.send_ascii_command(' '.join(args), 1)
                for line in reply:
                    print(line)
            except TimeoutException:
                pass

        elif command.startswith('_'):
            # everything after the '_' is interpreted by the pybind client
            try:
                reply = getattr(client._aura_client_impl, command[1:])(*[eval(a) for a in args])
                print(reply)
            except TimeoutException:
                pass

        else:
            raise InvalidCommand(f"invalid command: {command} {' '.join(args)}")

    except SelectClientException:
        raise

    except InvalidCommand:
        raise

    except Exception as exc:
        raise InvalidCommand(str(exc))

    return False


def process_command_line(client, command_line_str):
    """
    Processes a command line input.
    :param client: AuraClient instance
    :param command_line_str: one or many ';' separated commands
    :return:
    """
    commands = command_line_str.split(';')

    for command_str in commands:
        command_str = command_str.strip()
        if command_str:
            exit_requested = parse_command(client, *command_str.split())
            if exit_requested:
                return True

    return False


def _run_console_loop(port_name='', aura_id=None, initial_command=None, no_loop=False):
    """
    The main loop of the command line interface

    :param port_name: serial port to connect to for communication with AuraActuator.
                      Can be left empty for auto-detection.
    :param initial_command: an optional command to run at startup.
    """
    input_str = initial_command
    armed_exit = False

    with auraclient.AuraClient(port_name=port_name, aura_id=aura_id) as client:

        name = client._aura_client_impl.pull_name()
        print(f'Connected to {name if len(name) else "<no name>"} '
              f'on serial port: {client.get_port_name()}')
        print()
        if not no_loop:
            print_basic_usage()
            print()

        command_line_str = input_str
        while client.is_connected():
            try:
                if command_line_str is not None:
                    armed_exit = False
                    try:
                        exit_requested = process_command_line(client, command_line_str)
                        if exit_requested:
                            break

                    except InvalidCommand as exc:
                        client.stop()
                        print(exc, '- stopping')

                if no_loop:
                    return

                input_str = input('aura>> ')

                if input_str:
                    command_line_str = input_str
                armed_exit = False

            except KeyboardInterrupt:
                if sys.platform.startswith('linux'):
                    print("")
                if armed_exit:
                    try:
                        input_str = input('\nDo you really want to exit aura cli ([y]/n)?')
                    except KeyboardInterrupt:
                        if sys.platform.startswith('linux'):
                            print("")
                        input_str = 'y'

                    input_str = input_str.strip()
                    if not input_str or input_str.lower() == 'y':
                        break
                    else:
                        armed_exit = False
                        continue

                command_line_str = None
                armed_exit = True
                client.stop()
                print()


def run_console_loop(port_name='', aura_id=None, initial_command=None, no_loop=False):
    """
    The main loop of the command line interface

    :param port_name: serial port to connect to for communication with AuraActuator.
                      Can be left empty for auto-detection.
    :param aura_id: a specific aura actuator id to connect to - prompts if not specified
    :param initial_command: an optional command to run at startup.
    :param no_loop: exit right away (e.g. after executing initial command)
    """
    while True:
        try:
            return _run_console_loop(port_name=port_name,
                                     aura_id=aura_id,
                                     initial_command=initial_command,
                                     no_loop=no_loop)
        except SelectClientException as exc:
            initial_command = None
            port_name = exc.serial_port_name
            aura_id = exc.aura_id
        except Exception as exc:
            print_exc(exc)
            break
