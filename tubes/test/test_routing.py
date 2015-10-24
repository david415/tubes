# -*- test-case-name: tubes.test.test_routing -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for L{tubes.routing}.
"""

from __future__ import print_function

from zope.interface import implementer
from zope.interface.declarations import directlyProvides
from zope.interface.verify import verifyObject

from twisted.trial.unittest import SynchronousTestCase as TestCase
from twisted.python.failure import Failure

from ..itube import IDivertable, ITube, IFount
from ..tube import tube, series, Diverter
from ..routing import Routed, Router

from ..test.util import (TesterTube, FakeFount, FakeDrain, IFakeInput,
                         IFakeOutput, NullTube, PassthruTube, ReprTube,
                         FakeFountWithBuffer)

@tube
class Starter(object):
    """
    A tube that yields an integer.
    """

    def started(self):
        """
        Yield an integer.
        """
        yield 667

class EvenOdd(Router):
    outputType = Routed(int)
    def addRoutes(self):
        self.evenRoute = self.newRoute()
        self.oddRoute = self.newRoute()

    def received(self, item):
        if (item % 2) == 0:
            yield to(self.evenRoute, item)
        else:
            yield to(self.oddRoute, item)

            
class TestBasicRouter(TestCase):
    """
    Tests for L{Router}.
    """

    def setUp(self):
        self.ff = FakeFount()
        self.fd = FakeDrain()
        
    def test_basic_router(self):
        evenOddTube = EvenOdd()
        startTube = self.ff.flowTo(series(Starter()))
        startTube.flowTo(evenOddTube.drain)
        evenOddTube.addRoutes()
        evenOddTube.oddRoute.flowTo(self.fd)
        self.assertEquals(self.fd.received, [667])
