import argparse
import subprocess
import multiprocessing
import queue

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
    num_failed_attempts = 0

    # List of functions
    functions = [
        run_command,
        get_disk_io,
        get_memory,
        get_cpu_usage,
        get_network_counters
    ]

    # Setup dict of data values
    for i in range(5):
        measured_values[i] = queue.Queue()

    for i in range(args.c):
        processes = []
        for i in range(5):
            processes.append(multiprocessing.Process(target=functions[i], args=(args, measured_values[i])))

        for process in processes:
            process.start()

        for process in processes:
            process.join()

# Main function
if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    setup_runner(args)
