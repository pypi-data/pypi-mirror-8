# -*- coding: utf-8 -*-
from brasil.gov.portal.interfaces import IBrasilGov
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from zope.interface import alsoProvides

import unittest2 as unittest


class OverviewControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        # Como nao eh um teste funcional, este objeto
        # REQUEST precisa ser anotado com o browser layer
        alsoProvides(self.portal.REQUEST, IBrasilGov)

    def test_overview_controlpanel_view(self):
        """Validamos se o control panel esta acessivel"""
        view = api.content.get_view(
            name='overview-controlpanel',
            context=self.portal,
            request=self.portal.REQUEST,
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_overview_controlpanel_portal_padrao_version(self):
        """Validamos se temos a versão do Portal Padrão"""
        view = api.content.get_view(
            name='overview-controlpanel',
            context=self.portal,
            request=self.portal.REQUEST,
        )
        view = view.__of__(self.portal)
        content = view()
        self.assertIn(
            u'Portal Padrão 1.0.',
            content
        )
