import logging
import zipfile

from Acquisition import aq_inner

from five import grok

from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import IContentish

from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.decode import processInputs
from Products.statusmessages.interfaces import IStatusMessage

from sc.newsletter.creator import MessageFactory as _
from sc.newsletter.creator.utils import getOrCreatePersistentResourceDirectory
from sc.newsletter.creator.utils import getZODBThemes
from sc.newsletter.creator.config import NEWSLETTER_RESOURCE_NAME, MANIFEST_FORMAT

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(grok.View):
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.name('newsletter-creator')

    def update(self):
        super(View,self).update()
        context = aq_inner(self.context)
        self._path = '/'.join(context.getPhysicalPath())
        self.state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        self.tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.portal = getMultiAdapter((context, self.request), name=u'plone_portal_state')

    def get_template(self):
        """
        """
        templates = getZODBThemes()
        if templates:
            return templates[0]['template_content']

    def render(self):
        import pdb;pdb.set_trace()
        return self.get_template()