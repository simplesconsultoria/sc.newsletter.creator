import logging
import zipfile

from Acquisition import aq_inner

from five import grok

from zope.component import getMultiAdapter

from Products.CMFPlone.interfaces import IPloneSiteRoot

from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.decode import processInputs
from Products.statusmessages.interfaces import IStatusMessage

from sc.newsletter.creator import MessageFactory as _
from sc.newsletter.creator.utils import extractResourceName
from sc.newsletter.creator.utils import getOrCreatePersistentResourceDirectory
from sc.newsletter.creator.config import NEWSLETTER_RESOURCE_NAME, MANIFEST_FORMAT

logger = logging.getLogger('sc.newsletter.creator')

class View(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('newslettercreator-controlpanel')
    grok.require('cmf.ManagePortal')
    
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.context = aq_inner(self.context)
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.plone_tools = getMultiAdapter((self.context, self.request),
                                           name=u'plone_tools')
        self.catalog = self.plone_tools.catalog()

    def update(self):
        processInputs(self.request)
        self.errors = {}
        submitted = False
        form = self.request.form

        if 'form.button.Cancel' in form:
            self.redirect(_(u"Changes canceled."))
            return False

        if 'form.button.Import' in form:
            self.authorize()
            submitted = True

            replaceExisting = form.get('replaceExisting', False)
            newslettercreatorArchive = form.get('newslettercreatorArchive', None)

            newslettercreatorZip = None
            performImport = False

            try:
                newslettercreatorZip = zipfile.ZipFile(newslettercreatorArchive)
            except (zipfile.BadZipfile, zipfile.LargeZipFile,):
                logger.exception("Could not read zip file")
                self.errors['newslettercreatorArchive'] = _('error_invalid_zip',
                        default=u"The uploaded file is not a valid Zip archive"
                    )

            if newslettercreatorZip:
                resourceName = extractResourceName(newslettercreatorZip)
                newslettercreatorContainer = getOrCreatePersistentResourceDirectory()
                newslettercreatorExists = resourceName in newslettercreatorContainer

                if newslettercreatorExists:
                    if not replaceExisting:
                        self.errors['newslettercreatorArchive'] = _('error_already_installed',
                                u"This newsletter theme is already installed. Select 'Replace existing newsletter theme' and re-upload to replace it."
                            )
                    else:
                        del newslettercreatorContainer[resourceName]
                        performImport = True
                else:
                    performImport = True

            if performImport:
                newslettercreatorContainer.importZip(newslettercreatorZip)

        if submitted and not self.errors:
            IStatusMessage(self.request).add(_(u"Changes saved"))
        elif submitted:
            IStatusMessage(self.request).add(_(u"There were errors"), 'error')

        return True

    def authorize(self):
        authenticator = getMultiAdapter((self.context, self.request), name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized

    def redirect(self, message):
        IStatusMessage(self.request).add(message)
        portalUrl = getToolByName(self.context, 'portal_url')()
        self.request.response.redirect("%s/plone_control_panel" % portalUrl)
