import urllib

from DateTime import DateTime
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from OFS.interfaces import IOrderedContainer
from zope.interface.interfaces import IInterface
from zope.component import getMultiAdapter, queryUtility, getUtility
from zope.i18n import translate
from zope.size import byteDisplay

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.memoize import instance

from atreal.filecart import FileCartMessageFactory as _
from atreal.filecart import interfaces
from atreal.filecart.content import LineItemFactory
from atreal.filecart.browser.controlpanel import IFileCartSchema
from atreal.filecart.browser.tableview import Table, TableKSSView
from atreal.filecart.interfaces import IFileCartProvider
from atreal.filecart.browser.filecartzip import FileCartZip


class CartProvider (BrowserView) :
    """
    """
    msg = {
        'noSelection': _(u'fc_noselection',u"Your selection is empty. Nothing to delete."),
        'addOk': _(u'fc_addok',u"Your selection has been correctly added to your Cart."),
        'deleteOk': _(u'fc_deleteok',u"Your selection has been correctly deleted."),
        'alreadyExist': _(u'fc_alreadyexist',u"This element already exists in your Cart."),
        'notCartable': _(u'fc_notcartable',u"This element can't be added to your Cart."),
        'emptyOk': _(u'fc_emptyok',u"Your cart is now empty."),
        'isEmpty': _(u'fc_isempty',u"Your cart is empty. You can't do this action."),
        'download': _(u'fc_download',u"Normally you download your cart with this action."),
        'notInCart': _(u'fc_notincart',u"This element not exists in your Cart."),
    }

    _cart = None
    __filecartzip__ = FileCartZip

    @property
    def cart(self):
        if self._cart is not None:
            return self._cart

        cart_manager = getUtility (interfaces.ICartUtility)
        self._cart = cart_manager.get (self.context, create=True)
        return self._cart

    @property
    def _options(self):
        _siteroot = queryUtility (IPloneSiteRoot)
        return IFileCartSchema (_siteroot)

    def isCartable(self):
        return interfaces.IFileCartable.providedBy(self.context)

    def isEmpty(self):
        return self.cart.size () == 0

    def isContextAlreadyInCart(self):
        return IFileCartProvider(self.context).isInCart()

    def isObjectAlreadyInCart(self, obj):
        return IFileCartProvider(obj).isInCart()

    def getSize(self):
        return self.cart.size ()

    def getLastItemUID(self):
        return self.cart.last_item

    def getLinkAddToCart(self):
        return self.context.absolute_url() + '/@@filecart-cart?add_item=true'

    def getLinkToCart(self):
        return self.context.absolute_url() + '/@@filecart-cart'

    def getLinkToContext(self):
        return self.context.absolute_url() + '/view'

    def clearCart(self):
        cart_manager = getUtility (interfaces.ICartUtility)
        cart_manager.destroy (self.context)
        self.context.plone_utils.addPortalMessage (self.msg['emptyOk'])

    def delFromCart(self, fieldname=None):
        if IFileCartProvider(self.context).delFromCart(fieldname=fieldname) is False:
            self.context.plone_utils.addPortalMessage(self.msg['notInCart'])
        else:
            self.context.plone_utils.addPortalMessage(self.msg['deleteOk'])

    def delFromCartMulti(self):
        if self.request.has_key ('uids'):
            uids = self.request.form ['uids']
            for uid in uids:
                if '-' in uid: # we delete only an additional content
                    uuid, fieldname = uid.split('-')
                    self.cart[uuid].additional_attachments.remove(fieldname)
                else:
                    self.cart.__delitem__(uid)
            self.context.plone_utils.addPortalMessage(self.msg['deleteOk'])
        else:
            self.context.plone_utils.addPortalMessage(self.msg['noSelection'])

    def _cartContents(self):
        result = []
        for uid, item in self.cart.items ():
            pc = self.context.portal_catalog(UID=uid)
            if len(pc) != 0:
                result.append({'brain': pc[0],
                               'additional_attachments': getattr(item, 'additional_attachments', []),
                               'scales': getattr(item, 'scales', ['_source'])})

        return result

    def downloadCart(self):
        if self.isEmpty():
            self.context.plone_utils.addPortalMessage(self.msg['isEmpty'])
        else:
            contents = self._cartContents()
            self.__filecartzip__(self.request, contents)
            user = getSecurityManager().getUser().getId()
            comment = dict(
                user=user,
                date=DateTime(),
                comment=self.request.form.get('filecart_download_comment', ''),)

            filecartcommentsutility = getUtility(interfaces.IFileCartCommentsUtility)
            filecartcommentsutility.commentDownload(self.context, contents, comment)
            self.context.plone_utils.addPortalMessage(self.msg['download'])

    def addToCart(self):
        # create a line item and add it to the cart
        if self.isCartable():
            if IFileCartProvider(self.context).addToCart() is False:
                self.context.plone_utils.addPortalMessage(self.msg['alreadyExist'])
            else:
                self.context.plone_utils.addPortalMessage(self.msg['addOk'])
        else :
            self.context.plone_utils.addPortalMessage(self.msg['notCartable'])

    def addToCartMulti(self, obj):
        # create a line item and add it to the cart
        if self.isObjectAlreadyInCart(obj):
            self.context.plone_utils.addPortalMessage(self.msg['alreadyExist'])
        else:
            item_factory = LineItemFactory(self.cart, obj)
            item_factory.create()


class CartActionProvider(BrowserView):
    """
    """

    def isCartable(self):
        """
        """
        return interfaces.IFileCartable.providedBy(self.context)

    def isInCart(self):
        """
        """
        return interfaces.IFileCartProvider(self.context).isInCart()


class CartContentsTable(object):
    """
    The foldercontents table renders the table and its actions.
    """
    _cart = None

    __table__ = Table
    pagesize = 20
    ispreviewenabled = True

    def __init__(self, context, request):
        self.context = context
        self.request = request
        url = self.context.absolute_url()
        view_url = url + '/@@filecart-cart'
        self.table = self.__table__(request, url, view_url, self.items,
                           show_sort_column=self.show_sort_column,
                           buttons=self.buttons, pagesize=self.pagesize,
                           ispreviewenabled=self.ispreviewenabled)

    def render(self):
        return self.table.render()

    @property
    def cart(self):
        if self._cart is not None:
            return self._cart

        cart_manager = getUtility(interfaces.ICartUtility)
        self._cart = cart_manager.get(self.context, create=True)
        return self._cart

    def isOverrideAlbumViewInstalled(self):
        """
        """
        if queryUtility(IInterface, name=u'atreal.override.albumview.IOverrideAlbumViewSite', default=False):
            return True

        return False

    def isRichFileImageInstalled(self):
        """
        """
        if queryUtility(IInterface, name=u'atreal.richfile.image.IRichFileImageSite', default=False):
            return True

        return False

    @property
    @instance.memoize
    def items(self):
        """
        """
        context, request = self.context, self.request
        plone_utils = getToolByName(context, 'plone_utils')
        portal_workflow = getToolByName(context, 'portal_workflow')
        getTitleForStateOnType = portal_workflow.getTitleForStateOnType
        portal_properties = getToolByName(context, 'portal_properties')
        site_properties = portal_properties.site_properties
        mimetypes_registry = getToolByName(context, 'mimetypes_registry')
        portal_url = getToolByName(context, 'portal_url')()
        portal_catalog = getToolByName(context, 'portal_catalog')

        use_view_action = site_properties.getProperty('typesUseViewActionInListings', ())

        brains_image_uid = []
        if self.isRichFileImageInstalled() == True:
            brains_image = portal_catalog(object_provides='atreal.richfile.image.interfaces.IImage')
            for brain_image in brains_image:
                brains_image_uid.append(brain_image.UID)

        albumview = False
        if self.isOverrideAlbumViewInstalled() == True:
            albumview = True

        results = []
        i = -1
        for uid, item in self.cart.items():
            i += 1
            pc = portal_catalog(UID=uid)
            table_row_class = "draggable "
            table_row_class += (i + 1) % 2 == 0 and "even" or "odd"

            if len(pc) == 0:
                table_row_class += " deleted"
                results.append(dict(
                    UID = uid,
                    id = item.name,
                    title_or_id = item.name,
                    is_deleted = True,
                    table_row_class = table_row_class,
                ))
            else:
                brain = pc[0]

                url = brain.getURL()
                path = brain.getPath or "/".join(brain.getPhysicalPath())

                type_class = 'contenttype-' + plone_utils.normalizeString(
                    brain.portal_type)

                review_state = brain.review_state
                state_class = 'state-' + plone_utils.normalizeString(review_state)
                relative_url = brain.getURL(relative=True)
                obj_type = brain.portal_type

                is_expired = context.isExpired(brain)
                state_title = getTitleForStateOnType(review_state, obj_type)
                quoted_id = urllib.quote_plus(brain.getId)

                if obj_type in use_view_action:
                    view_url = url + '/view'
                else:
                    view_url = url

                if brain.UID in brains_image_uid:
                    thumb = url+'/rfimage/thumb'
                elif brain.portal_type == "Image":
                    thumb = url+'/image_thumb'
                elif albumview:
                    thumb = "%s/rf_%s" % (portal_url, brain.getIcon)
                else:
                    thumb = False

                object_info = dict(
                    UID=brain.UID,
                    url=url,
                    id=brain.getId,
                    quoted_id=quoted_id,
                    path=path,
                    title_or_id=brain.pretty_title_or_id(),
                    description=brain.Description,
                    obj_type=obj_type,
                    size=brain.getObjSize,
                    icon=brain.getIcon,
                    type_class=type_class,
                    wf_state=review_state,
                    state_title=getTitleForStateOnType(review_state, obj_type),
                    state_class=state_class,
                    folderish=brain.is_folderish,
                    relative_url=relative_url,
                    view_url=view_url,
                    table_row_class=table_row_class,
                    thumb=thumb,
                    is_expired=is_expired,
                    is_deleted=False,
                    is_additional=False,
                    fieldname=None,
                    lineitem=item,
                    brain=brain,
                )
                results.append(object_info)

                # ##### additional fields # #########
                if hasattr(item, 'additional_attachments'):
                    obj = brain.getObject()
                    for fieldname in item.additional_attachments:
                        i += 1
                        table_row_class = "additional draggable "
                        table_row_class += (i + 1) % 2 == 0 and "even" or "odd"
                        if len(pc) == 0:
                            table_row_class += " deleted"
                            results.append(dict(
                                UID=uid,
                                id=item.name + '-' + fieldname,
                                title_or_id="%s (%s)" % (item.name, fieldname),
                                is_deleted=True,
                                table_row_class=table_row_class,
                            ))
                        else:

                            state_class = 'state-' + plone_utils.normalizeString(review_state)
                            relative_url = brain.getURL(relative=True)
                            obj_type = obj.portal_type
                            view_url = obj_type in use_view_action and (url + '/view') or url

                            field = obj.getField(fieldname)
                            value = field.get(obj)
                            filename = value.filename
                            icon = mimetypes_registry.lookupExtension(filename).icon_path
                            size = byteDisplay(value.get_size())
                            size = translate(size, context=request, target_language='en')

                            type_class = 'contenttype-' + plone_utils.normalizeString(
                                brain.portal_type) + '-' + field.type
                            # for the moment, content sizes are not translated,
                            # so we don't translate additional fields sizes

                            attachment_info = dict(
                                UID='%s-%s' % (brain.UID, fieldname),
                                url=url,
                                id='%s-%s' % (brain.getId, fieldname),
                                quoted_id='%s-%s' % (quoted_id, fieldname),
                                path=path,
                                title_or_id=filename,
                                description="",
                                obj_type=field.type,
                                size=size,
                                icon=icon,
                                type_class=type_class,
                                wf_state=review_state,
                                state_title=state_title,
                                state_class=state_class,
                                folderish=False,
                                relative_url=relative_url,
                                view_url="%s/at_download/%s" % (url, fieldname),
                                table_row_class=table_row_class,
                                thumb=False,
                                is_expired=is_expired,
                                is_deleted=False,
                                is_additional=True,
                                fieldname=fieldname,
                                lineitem=item,
                                brain=brain,
                            )
                            results.append(attachment_info)

        return results

    @property
    def orderable(self):
        """
        """
        return IOrderedContainer.providedBy(self.context)

    @property
    def show_sort_column(self):
        return self.orderable and self.editable

    @property
    def editable(self):
        """
        """
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        return context_state.is_editable()

    @property
    def buttons(self):
        buttons = []
        portal_actions = getToolByName(self.context, 'portal_actions')
        button_actions = portal_actions.listActionInfos(object=aq_inner(self.context), categories=('cart_actions', ))

        # Do not show buttons if there is no data, unless there is data to be
        # pasted
        if not len(self.items):
            if self.context.cb_dataValid():
                for button in button_actions:
                    if button['id'] == 'paste':
                        return [self.setbuttonclass(button)]
            else:
                return []

        for button in button_actions:
            # Make proper classes for our buttons
            if button['id'] != 'paste' or self.context.cb_dataValid():
                buttons.append(self.setbuttonclass(button))
        return buttons

    def setbuttonclass(self, button):
        if button['id'] == 'paste':
            button['cssclass'] = 'standalone'
        else:
            button['cssclass'] = 'context'
        return button


class FileCartView(CartProvider) :
    """
    """

    __table__ = CartContentsTable

    def __call__(self):
        if self.request.has_key('cart.actions.delete'):
            self.delFromCartMulti()
        elif self.request.has_key('cart.actions.clear'):
            self.clearCart()
        elif self.request.has_key('cart.actions.download'):
            self.downloadCart()
        elif self.request.has_key('add_item'):
            self.addToCart()
        elif self.request.has_key('del_item'):
            self.delFromCart(fieldname=self.request.get('fieldname', False))
        elif self.request.has_key('add_items'):
            reference_tool = getToolByName(self.context, 'reference_catalog')
            if self.request.form.has_key('choix[]'):
                listchoix = self.request.form['choix[]']
                if type(listchoix) == str:
                    self.addToCartMulti(reference_tool.lookupObject(listchoix))
                else:
                    for uuid in listchoix:
                        self.addToCartMulti(reference_tool.lookupObject(uuid))

        return super(FileCartView, self).__call__()

    @property
    def table(self):
        return self.__table__(self.context, self.request)

    def contents_table (self):
        return self.table.render()

    def icon(self):
        """
        """
        ploneview = getMultiAdapter((self.context, self.request), name="plone")
        icon = ploneview.getIcon(self.context)
        return icon.html_tag()


class FileCartKSSView(TableKSSView):
    table = CartContentsTable
