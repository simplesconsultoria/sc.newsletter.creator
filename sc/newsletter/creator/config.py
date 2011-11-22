# -*- coding: utf-8 -*-

__author__ = """'Simples Consultoria'"""
__docformat__ = 'plaintext'

from plone.resource.manifest import ManifestFormat

PROJECTNAME = 'sc.newsletter.creator'

NEWSLETTER_RESOURCE_NAME = 'newslettercreator'

TEMPLATE_FILENAME = 'newsletter.pt'

MANIFEST_FORMAT = ManifestFormat(NEWSLETTER_RESOURCE_NAME,
        keys=['title', 'description','template','prefix'],)

