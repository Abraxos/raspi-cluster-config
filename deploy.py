from subprocess import call

print("NOTE: It is highly recommended that you run `raspi-config` before running this program...")
response = raw_input("Do you wish to run `raspi-config`? [Y/n]: ")
if response in ['', 'Y', 'yes', 'YES', 'Yes', 'y']:
    call(('raspi-config'))
elif response in ['N', 'no', 'NO', 'No', 'n']:
    print("Continuing without calling `raspi-config`...")
else:
    print("Response not understood... Exiting.")
    exit(1)

print("Installing pre-requisites:")
call(('apt','install','python-dev','gcc','g++','emacs','htop','tmux','mc'))
call(('apt', 'install', 'libcr-dev', 'mpich2', 'mpich2-doc'))
call(('wget https://bootstrap.pypa.io/get-pip.py'))
call(('python', 'get-pip.py'))
call(('pip','install','twisted','libtmux','mpi4py'))
