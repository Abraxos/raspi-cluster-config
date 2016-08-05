from socket import gethostname

from twisted.application import internet, service
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

'''
Run using twistd:

$ twistd -ny udpbroadcast.py
'''

HOSTNAME = gethostname()

class MulticastSender(DatagramProtocol):
    noisy = False

    def __init__(self, port=1871):
        self.port = port

    def startProtocol(self):
        self.transport.setBroadcastAllowed(True)

    def sendPing(self):
        self.transport.write(HOSTNAME, ('<broadcast>', self.port))

    def datagramReceived(self, datagram, addr):
        print "RECV:" + datagram + " from: " + addr
        if datagram == 'professor ack':
            print("Professor has found us!")
            reactor.stop()

class Broadcaster(object):
    def ping(self, proto):
        proto.sendPing()

    def makeService(self):
        application = service.Application('Broadcaster')
        root = service.MultiService()
        root.setServiceParent(application)
        proto = MulticastSender(port=1871)
        root.addService(internet.UDPServer(1871, proto))
        root.addService(internet.TimerService(1, self.ping, proto))
        return application

protocol = MulticastSender(port=1871)
lc = LoopingCall(protocol)
reactor.listenUDP(1871, protocol)
reactor.run()
