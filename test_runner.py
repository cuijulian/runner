from subprocess import run, PIPE

import runner


def test_should_run_command_n_times_successfully():
    runner.exit_codes = []
    parser = runner.create_parser()
    args = parser.parse_args(['true', '-c', '5'])
    exit_codes = runner.setup_runner(args)
    assert len(exit_codes) == 5


def test_should_run_command_n_times_unsuccessfully():
    runner.exit_codes = []
    parser = runner.create_parser()
    args = parser.parse_args(['false', '-c', '5', '--failed-count', '3'])
    exit_codes = runner.setup_runner(args)
    assert len(exit_codes) == 3


def test_should_create_log_file():
    runner.create_log('log', 0, 'data')
    command_return = run("grep data log0.log", shell=True)
    assert command_return.returncode == 0


def test_should_create_sys_trace_logs_when_fail():
    runner.exit_codes = []
    parser = runner.create_parser()
    args = parser.parse_args(['false', '-c', '5', '--failed-count', '1',
                              '--sys-trace'])
    runner.setup_runner(args)
    command_return = run("find . -name 'sys_trace_*.log' | wc -l", shell=True,
                         stdout=PIPE)
    assert int(command_return.stdout) == 4


def test_should_create_call_trace_logs_when_fail():
    runner.exit_codes = []
    parser = runner.create_parser()
    args = parser.parse_args(['false', '-c', '5', '--failed-count', '3',
                              '--call-trace'])
    runner.setup_runner(args)
    command_return = run("find . -name 'call_trace*.log' | wc -l", shell=True,
                         stdout=PIPE)
    assert int(command_return.stdout) == 3


def test_should_create_log_trace_logs_when_fail():
    runner.exit_codes = []
    parser = runner.create_parser()
    args = parser.parse_args(['false', '-c', '5', '--failed-count', '2',
                              '--log-trace'])
    runner.setup_runner(args)
    command_return = run("find . -name 'log_trace*.log' | wc -l", shell=True,
                         stdout=PIPE)
    assert int(command_return.stdout) == 2
