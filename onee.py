import sys
import subprocess

# COMMAND EXECUTION
def execute(commands):
    """Creates a file to execute the given commands"""
    script_name = 'sandbox.sh'
    with open(script_name, 'w+') as fp:
        for command in commands:
            fp.write('%s\n' % (command))
    if subprocess.call(['sh', script_name]) > 0:
        raise RuntimeError()
    else:
        subprocess.call(['rm', script_name])

# MAIN COMMANDS

def compress(inlet):
    """Creates a compression script and runs it."""
    echo = 'echo %s' % (inlet)
    commands = [echo]
    execute(commands)


def decompress(inlet):
    pass

if __name__ == '__main__':
    if sys.argv[1] == 'compress':
        compress(sys.argv[2])
    elif sys.argv[1] == 'decompress':
        raise NotImplementedError()
    else:
        raise RuntimeError()
