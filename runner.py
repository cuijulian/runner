import argparse
import subprocess
import queue
import psutil
import signal
import sys

import collections

exit_codes = []


# Specifies the accepted command line args for the script
def create_parser():
    parser = argparse.ArgumentParser(description='Outputs summary of command execution.')

    parser.add_argument('COMMAND',
                        help='the command to be run')

    parser.add_argument('-c', type=int, default=1,
                        help='number of times to run the given command')

    parser.add_argument('--failed-count', type=int, default=0,
                        help='number of allowed failed command invocation attempts before giving up')

    parser.add_argument('--sys-trace', action='store_true',
                        help='creates a log for: Disk IO, Memory, Processes/CPU Usage, Network Card Package Counters')

    parser.add_argument('--call-trace', action='store_true',
                        help='for each failed execution, add a log with all the system calls ran by the command')

    parser.add_argument('--log-trace', action='store_true',
                        help='for each failed execution, add the command output logs')

    parser.add_argument('--debug', action='store_true',
                        help='show each instruction executed by the script')

    return parser


# Gets return codes and other command data
def setup_runner(args):
    measured_values = []
    completed_processes = []
    global exit_codes
    num_failed_attempts = 0

    # Setup list of data value queues
    for i in range(5):
        measured_values.append(queue.Queue())

    for i in range(args.c):

        run_command(args, measured_values[0])
        get_disk_io(measured_values[1])
        get_memory(measured_values[2])
        get_cpu_usage(measured_values[3])
        get_network_counters(measured_values[4])

        # Get CompletedProcess from subprocess.run()
        completed_processes.append(measured_values[0].get())

        # Store command exit code
        exit_codes.append(completed_processes[-1].returncode)

        stdout_log = str(completed_processes[-1].stdout.decode())
        stderr_log = str(completed_processes[-1].stderr.decode())

        # If command failed, create logs
        if exit_codes[-1] != 0:
            if args.sys_trace:
                create_log('disk_io', num_failed_attempts, measured_values[1].get())
                create_log('memory', num_failed_attempts, measured_values[2].get())
                create_log('cpu_usage', num_failed_attempts, measured_values[3].get())
                create_log('network_counters', num_failed_attempts, measured_values[4].get())

            if args.call_trace:
                create_log('call_trace', num_failed_attempts, stderr_log)

            if args.log_trace:
                create_log('log_trace', num_failed_attempts, f'stdout: {stdout_log}\nstderr: {stderr_log}')

            num_failed_attempts += 1

            # Max failed attempts reached
            if num_failed_attempts == args.failed_count and args.failed_count > 0:
                print('The command has reached its maximum failed attempts.')
                break


# Runs command
def run_command(args, queue):
    if args.call_trace:
        command = "strace -c {}".format(args.COMMAND)
    else:
        command = args.COMMAND

    completed_process = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    queue.put(completed_process)


# Gets disk IO data
def get_disk_io(queue):
    disk_io_data = psutil.disk_io_counters()
    queue.put(str(disk_io_data))


# Gets memory data
def get_memory(queue):
    memory_data = psutil.virtual_memory()
    queue.put(str(memory_data))


# Gets cpu usage data
def get_cpu_usage(queue):
    cpu_usage = psutil.cpu_percent(interval=0.1)
    queue.put(str(cpu_usage))


# Gets network card package counters
def get_network_counters(queue):
    network_counters = psutil.net_io_counters()
    queue.put(str(network_counters))


# Creates log when command fails
def create_log(file_name, file_number, data):
    with open(f'{file_name}{file_number}.log', 'w') as f:
        f.write(data)


# Prints command summary
def print_summary():
    global exit_codes
    exit_code_occurrences = collections.Counter(exit_codes)

    for code, count in exit_code_occurrences.items():
        print(f'The return code {code} appears {count} times')

    code, count = exit_code_occurrences.most_common(1)[0]
    print(f'The most common return code is {code}, which appears {count} times')


# Handle signals
def signal_handler(signal, frame):
    print(f'Program was interrupted by signal number {signal}')
    print_summary()
    sys.exit(0)


# Main function
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    parser = create_parser()
    args = parser.parse_args()

    setup_runner(args)
    print_summary()
