import argparse
import subprocess

def create_parser():
    parser = argparse.ArgumentParser(description='Outputs summary of command execution.')

    parser.add_argument('command',
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

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
