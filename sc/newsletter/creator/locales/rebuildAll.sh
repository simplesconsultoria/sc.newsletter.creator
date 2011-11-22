#!/bin/bash
# kudos to Products.Ploneboard for the base for this file
# ensure that when something is wrong, nothing is broken more than it should...
set -e

# first, create some pot containing anything
i18ndude rebuild-pot --pot sc.newsletter.creator.pot --create sc.newsletter.creator --merge manual.pot ..

# finally, update the po files
i18ndude sync --pot sc.newsletter.creator.pot  `find . -iregex '.*sc.newsletter.creator\.po$'|grep -v plone`

