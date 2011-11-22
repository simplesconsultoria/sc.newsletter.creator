import logging
import zipfile

from Acquisition import aq_inner
from Acquisition import aq_get

from five import grok

from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import IContentish

from AccessControl import getSecurityManager
from Products.PageTemplates.Expressions import SecureModuleImporter

from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.decode import processInputs
from Products.statusmessages.interfaces import IStatusMessage

from sc.newsletter.creator import MessageFactory as _
from sc.newsletter.creator.utils import getOrCreatePersistentResourceDirectory
from sc.newsletter.creator.utils import getZODBThemes
from sc.newsletter.creator.config import NEWSLETTER_RESOURCE_NAME, MANIFEST_FORMAT

from zope.pagetemplate.pagetemplate import PageTemplate

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

    def get_context(self, instance, request, **kw):
        pt = PageTemplate()
        namespace = pt.pt_getContext()
        namespace['request'] = request
        namespace['view'] = instance
        namespace['context'] = context = instance.context

        # get the root
        obj = self.context
        root = None
        meth = aq_get(obj, 'getPhysicalRoot', None)
        if meth is not None:
            root = meth()

        namespace.update(here=obj,
                         # philiKON thinks container should be the view,
                         # but BBB is more important than aesthetics.
                         container=obj,
                         root=root,
                         modules=SecureModuleImporter,
                         traverse_subpath=[],  # BBB, never really worked
                         user = getSecurityManager().getUser()
                        )
        return namespace

    def render(self):
        pt = PageTemplate()
        pt.write(self.get_template())
        instance = self
        request = self.request
        namespace = self.get_context(instance, request)

        return pt.pt_render(namespace)