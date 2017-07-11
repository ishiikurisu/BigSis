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
    box = ''
    for part in file_parts:
        box += part + '/'
        commands.append('mkdir ' + box)
    commands.append('cd box')
    for part in file_parts[:-1]:
        commands.append('cd ' + part)
    commands.append('tar czpvf - {0} | split -d -b 50M - tardisk'.format(file_parts[-1]))
    for _ in range(len(file_parts)):
        commands.append('cd ..')
    file_path = '/'.join(file_parts[:-1])
    commands.append('mv box/{0}/tardisk* {1}'.format(file_path, inlet))
    execute(commands)

def decompress(inlet):
    """Creates a decompression script and runs it."""
    commands = [ ]
    file_parts = inlet.split('/')
    outlet = file_parts[-1]
    for part in file_parts:
        commands.append('cd ' + part)
    commands.append('cat tardisk* | tar xzpvf - ')
    dots = ''
    for _ in range(len(file_parts)):
        dots += '../'
    commands.append('mv %s %s' % (outlet, dots))
    for _ in range(len(file_parts)):
        commands.append('cd ..')
    box = 'box/'
    for part in file_parts[0:-1]:
        box += part + '/'
        commands.append('mkdir ' + box)
    commands.append('mv %s %s' % (outlet, box))
    execute(commands)

if __name__ == '__main__':
    if sys.argv[1] == 'compress':
        compress(sys.argv[2])
    elif sys.argv[1] == 'decompress':
        decompress(sys.argv[2])
    else:
        raise RuntimeError()
