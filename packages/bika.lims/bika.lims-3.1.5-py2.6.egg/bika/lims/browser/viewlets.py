from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter


class DocumentActionsViewlet(ViewletBase):

    """Overload the default to print pretty icons """

    index = ViewPageTemplateFile("templates/document_actions.pt")

    def render(self):
        portal_factory = getToolByName(self.context, 'portal_factory')
        if portal_factory.isTemporary(self.context):
            return self.index()
        self.actions = []
        portal_actions = getToolByName(self.context, 'portal_actions')
        actions = portal_actions.listFilteredActionsFor(self.context)
        if 'document_actions' in actions:
            for action in actions['document_actions']:
                self.actions.append(action)
        return self.index()


class PathBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/path_bar.pt')

    def update(self):
        super(PathBarViewlet, self).update()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter((self.context, self.request),
                                           name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()


class AuthenticatorViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/authenticator.pt')
