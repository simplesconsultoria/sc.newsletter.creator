# -*- coding: utf-8 -*-
from zope import component
import logging
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup import interfaces as gsinterfaces
from Products.GenericSetup.upgrade import listUpgradeSteps

from Products.ZCatalog.ProgressHandler import ZLogHandler

logger = logging.getLogger('sc.newsletter.creator')
def upgrade0to1000(context):
    ''' Upgrade to profile version 1000
    '''
    setup = getToolByName(context, 'portal_setup')
    catalog = getToolByName(context,'portal_catalog')
    portal_properties = getToolByName(context,'portal_properties')
    qi = getToolByName(context,'portal_quickinstaller')
    
    # # Install dependencies
    # dependencies = [
    #                 ('Products.ATGoogleVideo',0,0,'Products.ATGoogleVideo:default'),
    #                ]
    # logger.info('Install dependencies')
    # for name,locked,hidden,profile in dependencies:
    #     qi.installProduct(name, locked=locked, hidden=hidden, profile=profile)
      
    # # Execute a profile
    # profiles = ['profile-sc.newsletter.creator:initializeCatalog',
    #            ]
    # logger.info('Run profiles')
    # for profile in profiles:
    #     setup.runAllImportStepsFromProfile(profile)
    
    