# -*- coding: utf-8 -*-
import logging

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.upgrade import listUpgradeSteps

from Products.CMFQuickInstallerTool.interfaces import INonInstallable

_PROJECT = 'sc.newsletter.creator'
_PROFILE_ID = 'sc.newsletter.creator:default'

class HiddenProducts(object):
    implements(INonInstallable)

    def getNonInstallableProducts(self):
        return ['plone.resources',]

#    def getNonInstallableProfiles(self):
#        return ['plone.resources:default',]

def doUpgrades(context):
    """ If exists, run migrations
    """
    if context.readDataFile('sc.newsletter.creator.txt') is None:
        return
    logger = logging.getLogger(_PROJECT)
    site = context.getSite()
    setup_tool = getToolByName(site,'portal_setup')
    version = setup_tool.getLastVersionForProfile(_PROFILE_ID)
    upgradeSteps = listUpgradeSteps(setup_tool,_PROFILE_ID, version)
    sorted(upgradeSteps,key=lambda step:step['sortkey'])

    for step in upgradeSteps:
        oStep = step.get('step')
        if oStep is not None:
            oStep.doStep(setup_tool)
            msg = "Ran upgrade step %s for profile %s" % (oStep.title,
                                                          _PROFILE_ID)
            setup_tool.setLastVersionForProfile(_PROFILE_ID, oStep.dest)
            logger.info(msg)