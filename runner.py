import subprocess
import sys

if __name__ == "__main__":

    count = 1
    num_failed_attempts = 0
    sys_trace_option = call_trace_option = log_trace_option = debug_option = help_option = False

    # Retrieve options from command line args
    i = 1
    command_line = []
    while i < len(sys.argv):
        if sys.argv[i] == '-c':
            count = int(sys.argv[i + 1])
            i += 2
            continue
        elif sys.argv[i] == '--failed-count':
            num_failed_attempts = int(sys.argv[i + 1])
            i += 2
            continue
        elif sys.argv[i] == '--sys-trace':
            sys_trace_option = True
        elif sys.argv[i] == '--call-trace':
            call_trace_option = True
        elif sys.argv[i] == '--log-trace':
            log_trace_option = True
        elif sys.argv[i] == '--debug':
            debug_option = True
        elif sys.argv[i] == '--help':
            help_option = True
        else:
            command_line.append(sys.argv[i])

        i += 1

    for i in range(count):
        subprocess.run(command_line)
