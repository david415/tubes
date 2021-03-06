from tubes.tube import Tube
from tubes.framing import stringsToNetstrings
from tubes.protocol import factoryFromFlow
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.defer import Deferred

def echoTubeFactory(fount, drain):
    return (fount.flowTo(Tube(stringsToNetstrings()))
                 .flowTo(drain))

def main(reactor):
    endpoint = TCP4ServerEndpoint(reactor, 4321)
    endpoint.listen(factoryFromFlow(echoTubeFactory))
    return Deferred()

if __name__ == '__main__':
    from twisted.internet.task import react
    react(main, [])
