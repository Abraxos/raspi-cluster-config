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
call(('apt-get', 'update', '--fix-missing'))
call(('apt-get', 'update'))
call(('apt-get', 'upgrade', '-y'))
call(('apt-get', 'dist-upgrade', '-y'))
call(('apt','install','python-dev','gcc','g++','emacs','htop','tmux','mc'))
call(('apt', 'install', 'libcr-dev', 'mpich2', 'mpich2-doc'))
call(('wget', 'https://bootstrap.pypa.io/get-pip.py'))
call(('python', 'get-pip.py'))
call(('pip','install','twisted','libtmux','mpi4py'))

# Set up various files
with open('/home/pi/.cluster.log', 'w+') as logfile:
    logfile.write("Log initialized")

call(('chown','pi:pi','/home/pi/.cluster.log'))
call(('chmod','ugo+rwx','/home/pi/.cluster.log'))

print("NOTE: It is highly recommended that you run `raspi-config` before running this program...")
response = raw_input("Is this a professor node? [Y/n]: ")
if response in ['', 'Y', 'yes', 'YES', 'Yes', 'y']:
    print("Configuring professor node...")
    with open('/etc/rc.local','r+') as rc_file:
        contents = rc_file.readlines()
        line = 'python /home/pi/raspi-cluster-config-master/start-professor.py &> /home/pi/.cluster.log'
        if line not in contents:
            contents.insert(-2,line)
    with open('/etc/rc.local','w+') as rc_file:
        rc_file.write("".join(contents))
    print("Generating SSH keys (NOTE: the public key needs to be copied to the student nodes manually!)")
    call(('runuser', '-l', 'pi', '-c', '"ssh-keygen"'))
elif response in ['N', 'no', 'NO', 'No', 'n']:
    print("Configuring student node...")
    with open('/etc/rc.local','r+') as rc_file:
        contents = rc_file.readlines()
        line = 'python /home/pi/raspi-cluster-config-master/start-student.py &> /home/pi/.cluster.log'
        if line not in contents:
            contents.insert(-2,line)
    with open('/etc/rc.local','w+') as rc_file:
        rc_file.write("".join(contents))
else:
    print("Response not understood... Setup incomplete! Exiting.")
    exit(1)
print("Done! - Please configure the student nodes and reboot all of the cluster nodes.")
