# import for traverser adapter
from five import grok
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import IRequest


from plone.resource.traversal import ResourceTraverser

from sc.newsletter.creator.config import NEWSLETTER_RESOURCE_NAME

class NewsletterThemeTraverser(ResourceTraverser):
    """ Allows traveral to /++newslettercreator++<name> using ``plone.resource``
    to fetch in the ZODB.
    """

    name = NEWSLETTER_RESOURCE_NAME

#grok.global_adapter(NewsletterThemeTraverser,('*', IRequest,), ITraversable , name=u'newslettercreator')
