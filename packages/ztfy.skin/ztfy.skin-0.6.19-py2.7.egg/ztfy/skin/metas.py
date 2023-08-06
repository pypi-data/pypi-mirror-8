### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2012 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################


# import standard packages

# import Zope3 interfaces

# import local interfaces
from ztfy.skin.interfaces import ICustomBackOfficeInfoTarget
from ztfy.skin.layer import IZTFYBackLayer

# import Zope3 packages
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser.absoluteurl import absoluteURL

# import local packages
from ztfy.baseskin.metas import *
from ztfy.utils.traversing import getParent


class BaseContentMetasHeadersBackAdapter(object):
    """Base content back-office metas adapter"""

    adapts(Interface, IZTFYBackLayer)
    implements(IContentMetasHeaders)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def metas(self):
        result = []
        back_target = getParent(self.context, ICustomBackOfficeInfoTarget)
        if back_target is not None:
            back_info = removeSecurityProxy(back_target.back_interface)(back_target)
            if getattr(back_info, 'custom_icon', None):
                result.append(LinkMeta('icon', back_info.custom_icon.contentType,
                                       absoluteURL(back_info.custom_icon, self.request)))
            else:
                result.append(LinkMeta('icon', 'image/png', '/@@/favicon.ico'))
        else:
            result.append(LinkMeta('icon', 'image/png', '/@@/favicon.ico'))
        return result
