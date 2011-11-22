from zope.component import getUtility

from plone.resource.interfaces import IResourceDirectory
from plone.resource.manifest import extractManifestFromZipFile
from plone.resource.manifest import getZODBResources
from plone.resource.manifest import MANIFEST_FILENAME

from sc.newsletter.creator.config import MANIFEST_FORMAT
from sc.newsletter.creator.config import NEWSLETTER_RESOURCE_NAME
from sc.newsletter.creator.config import TEMPLATE_FILENAME

from Acquisition import aq_parent

def getOrCreatePersistentResourceDirectory():
    """ Obtain the 'theme' persistent resource directory, creating it if
    necessary.
    """

    persistentDirectory = getUtility(IResourceDirectory, name="persistent")
    if NEWSLETTER_RESOURCE_NAME not in persistentDirectory:
        persistentDirectory.makeDirectory(NEWSLETTER_RESOURCE_NAME)

    return persistentDirectory[NEWSLETTER_RESOURCE_NAME]

def extractResourceName(zipfile):
    """ 
    """
    resourceName, manifestDict = extractManifestFromZipFile(
        zipfile, MANIFEST_FORMAT)

    return resourceName

def isValidThemeDirectory(directory):
    """Determine if the given plone.resource directory is a valid newsletter theme
    directory
    """
    return directory.isFile(MANIFEST_FILENAME) or \
           directory.isFile(TEMPLATE_FILENAME)


def getZODBThemes():
    """Get a list of newletter themes stored in the ZODB.
    """

    resources = getZODBResources(MANIFEST_FORMAT, filter=isValidThemeDirectory)
    directory = getOrCreatePersistentResourceDirectory()
    themes = []
    for name, manifest in resources.items():
        title = name.capitalize().replace('-', ' ').replace('.', ' ')
        description = None
        template_link = u"/++%s++%s/%s" % (NEWSLETTER_RESOURCE_NAME, name, TEMPLATE_FILENAME,)
        template_content = directory[name].openFile(TEMPLATE_FILENAME).read()
        prefix = u"/++%s++%s" % (NEWSLETTER_RESOURCE_NAME, name,)

        if manifest is not None:
            title = manifest['title'] or title
            description = manifest['description'] or description
            template_link = manifest['template'] or template
            prefix = manifest['prefix'] or prefix


        themes.append(dict(name=name,
                           template_link=template_link,
                           template_content=template_content,
                           title=title,
                           description=description,
                            )
            )

    themes.sort(key=lambda x: x['title'])
    return themes