# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.upload
        self.loadZCML(package=collective.upload)
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.upload:default')
        self.applyProfile(portal, 'collective.upload:testfixture')

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.upload:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.upload:Functional',
)
