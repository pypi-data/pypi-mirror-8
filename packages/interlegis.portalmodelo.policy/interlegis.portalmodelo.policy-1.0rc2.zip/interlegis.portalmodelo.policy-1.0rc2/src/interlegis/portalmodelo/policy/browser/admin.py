# -*- coding:utf-8 -*-
from AccessControl import getSecurityManager
from AccessControl.Permissions import view as View
from Products.CMFCore.permissions import ManagePortal
from Products.CMFPlone.browser.admin import AddPloneSite as AddPloneSiteView
from Products.CMFPlone.browser.admin import Overview as OverviewView
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from Products.CMFPlone.interfaces import IPloneSiteRoot


class Overview(OverviewView):
    def sites(self, root=None):
        if root is None:
            root = self.context

        result = []
        secman = getSecurityManager()
        for obj in root.values():
            if IPloneSiteRoot.providedBy(obj):
                if secman.checkPermission(View, obj):
                    result.append(obj)
            elif obj.getId() in getattr(root, '_mount_points', {}):
                result.extend(self.sites(root=obj))
        return result

    def outdated(self, obj):
        mig = obj.get('portal_migration', None)
        if mig is not None:
            return mig.needUpgrading()
        return False

    def can_manage(self):
        secman = getSecurityManager()
        return secman.checkPermission(ManagePortal, self.context)

    def upgrade_url(self, site, can_manage=None):
        if can_manage is None:
            can_manage = self.can_manage()
        if can_manage:
            return site.absolute_url() + '/@@plone-upgrade'
        else:
            return self.context.absolute_url() + '/@@plone-root-login'


class AddPloneSite(AddPloneSiteView):

    def __call__(self):
        context = self.context
        form = self.request.form
        extensions = [i['id'] for i in self.profiles()['extensions'] if i.get('selected')]
        extension_ids = form.get('extension_ids', [])
        for extension in extension_ids:
            extensions.append(extension)
        # Dados do formulario
        site_id = form.get('site_id', 'portalmodelo')
        title = form.get('title_site', 'Portal Modelo')
        description = form.get('description_site', '')
        # Se o formulario tiver sido enviado, criaremos o site
        submitted = form.get('form.submitted', False)
        if submitted:
            # Criacao do site
            site = addPloneSite(
                context, site_id,
                title=title,
                description=description,
                profile_id=form.get('profile_id', _DEFAULT_PROFILE),
                extension_ids=extensions,
                setup_content=False,
                default_language='pt-br',
            )
            # Atualizacao de propriedades do site
            site.manage_changeProperties(
                title=title,
                description=description,
            )
            self.request.response.redirect(site.absolute_url())

        return self.index()
