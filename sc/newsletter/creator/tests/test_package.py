# -*- coding:utf-8 -*-
from zope.interface import implements, Interface
from zope.component import getUtility, getMultiAdapter

from sc.newsletter.creator.tests.base import TestCase

from Products.PloneTestCase.setup import default_user

from DateTime import DateTime

class DummyEvent(object):
    implements(IObjectEvent)
    
    def __init__(self, object):
        self.object = object

class TestPackage(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        # Create objects to be used in test
        self.portal.invokeFactory('Folder', 'foo')
    
    def testSomething(self): 
        self.assertEquals(1, 1)
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPackage))
    return suite
