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
    commands = [ ]
    file_parts = inlet.split('/')
    commands.append('cd box')
    for part in file_parts[:-1]:
        commands.append('cd ' + part)
    commands.append('tar czpvf - {0} | split -d -b 50M - tardisk'.format(file_parts[-1]))
    for _ in range(len(file_parts)):
        commands.append('cd ..')
    commands.append('pwd')
    file_path = '/'.join(file_parts[:-1])
    commands.append('mv box/{0}/tardisk* {1}'.format(file_path, inlet))
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
