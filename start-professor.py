from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from socket import gethostname
from subprocess import call
import libtmux

HOSTNAME = gethostname()
CLUSTER = {'student1':None, 'student2':None, 'student3':None}

class MulticastListener(DatagramProtocol):

    def startProtocol(self):
        self.transport.setTTL(5)
        self.transport.joinGroup("228.0.0.5")

    def datagramReceived(self, datagram, address):
        datagram = str(datagram)
        address = str(address)
        print("Datagram %s received from %s" % (datagram, address))

        if datagram in CLUSTER:
            CLUSTER[datagram] = address
            self.transport.write("professor ack", address)
        if all(CLUSTER['student1'], CLUSTER['student2'], CLUSTER['student3']):
            reactor.stop()

reactor.listenMulticast(1871, MulticastListener(), listenMultiple=True)
reactor.run()

for raspi in CLUSTER:
    print("{0} found at {1}".format(raspi, CLUSTER[raspi]))

# Once the IP addresses of all the students have been found, open up a TMUX
# window and SSH into them
call(('tmux', 'new-session', '-s', 'admin', '-n', 'admin'))
tmux_server = libtmux.Server()
session = server.find_where({ "session_name": "admin" })
window = session.attached_window
pane1 = window.attached_pane
pane2 = window.split_window(attach=False)
pane2.send_keys('ssh {0}'.format(CLUSTER['student1']))
pane3 = window.split_window(attach=False)
pane3.send_keys('ssh {0}'.format(CLUSTER['student2']))
pane4 = window.split_window(attach=False)
pane4.send_keys('ssh {0}'.format(CLUSTER['student3']))
