# -*- coding: utf-8 -*-
from Products.CMFPlone import interfaces as st_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implements

PROJECTNAME = 'brasil.gov.paginadestaque'


class HiddenProducts(object):
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return [
            u'sc.microsite',
        ]


class HiddenProfiles(object):
    implements(st_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.paginadestaque:uninstall',
            u'sc.microsite:default',
            u'sc.microsite:uninstall',
        ]
