# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from DateTime import DateTime
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from pd.contentrules.sms import messageFactory as _, logger
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable
from rg.prenotazioni.content.prenotazione import Prenotazione
from zope import schema
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.formlib import form
from zope.interface import Interface, implements


class ISMSFromFieldAction(Interface):

    """Definition of the configuration available for a mail action
    """
    message = schema.Text(
        title=_(u"SMS message"),
        description=_(
            'help_message',
            default=(
                u"Type in here the message that you want to mail. "
                u"Some defined content can be replaced:"
                u"${title} will be replaced by the title of the target item. "
                u"${url} will be replaced by the URL of the item. "
                u"${section_url} will be replaced by the URL of the content the rule is applied to. "  # noqa
                u"${section_name} will be replaced by the title of the content the rule is applied. "  # noqa
                u"${date} will be replace by the date of the content the rule is applied. "  # noqa
                u"${time} will be replace by the time of the content the rule is applied. "  # noqa
                u"${gate} will be replace by the gate value of the content the rule is applied. "  # noqa
                u"${type} will be replace by the type value of the content the rule is applied. "  # noqa
                u"to.")
        ),
        required=True
    )

    sms_domain = schema.TextLine(
        title=_(u"SMS email domain"),
        description=_(
            'sms_domain_help',
            default=u"The email domain name used to send sms messages"
        ),
        required=True
    )


class SMSFromFieldAction(SimpleItem):

    """
    The implementation of the action defined before
    """
    implements(ISMSFromFieldAction, IRuleElementData)

    message = u''
    sms_domain = u''

    element = u'pd.actions.SMSFromField'

    summary = _('action_summary',
                default=u'SMS to users defined in the mobile data field')


class SMSActionExecutor(object):

    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, ISMSFromFieldAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        self.portal = self.get_portal()
        self.mapping = self.get_mapping()

    def get_portal(self):
        '''Get's the portal object
        '''
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        return urltool.getPortalObject()

    def get_mapping(self):
        '''Return a mapping that will replace markers in the template
        '''
        plone = self.context.restrictedTraverse('@@plone')
        obj_title = safe_unicode(self.event.object.Title())
        event_url = self.event.object.absolute_url()
        section_title = safe_unicode(self.context.Title())
        section_url = self.context.absolute_url()
        date = DateTime(self.event.object.Date())
        gate = self.event.object.getGate()
        book_type = self.event.object.getTipologia_prenotazione()
        return {"url": event_url,
                "title": obj_title,
                "section_name": section_title,
                "section_url": section_url,
                "date": plone.toLocalizedTime(date),
                "time": plone.toLocalizedTime(date, time_only=True),
                "gate": gate,
                "type": book_type}

    def expand_markers(self, text):
        '''Replace markers in text with the values in the mapping
        '''
        for key, value in self.mapping.iteritems():
            if not isinstance(value, unicode):
                value = value.decode('utf-8')
            text = text.replace('${%s}' % key, value)
        return text

    def get_from(self):
        '''Get the from address
        '''
        from_address = self.portal.getProperty('email_from_address')
        if not from_address:
            raise ValueError('You must provide a source address for this '
                             'action or enter an email in the portal '
                             'properties')
        from_name = self.portal.getProperty('email_from_name')
        source = ("%s <%s>" % (from_name, from_address)).strip()
        return source

    def get_recipients(self):
        '''
        The mobile number for the SMS mail
        '''
        if not isinstance(self.event.object, Prenotazione):
            return []
        event_obj = self.event.object
        email = event_obj.getEmail()
        # Don't send an sms when we can send an email (which is cheaper!)
        if email:
            return []
        mobile = event_obj.getMobile()
        domain = self.element.sms_domain
        if not mobile or not domain:
            return []
        mobile = ''.join(mobile.split())
        return [mobile + '@' + domain]

    def get_mailhost(self):
        '''
        The recipients of this mail
        '''
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            error = 'You must have a Mailhost utility to execute this action'
            raise ComponentLookupError(error)
        return mailhost

    def __call__(self):
        '''
        Does send the mail to the SMS service
        '''
        mailhost = self.get_mailhost()

        source = self.get_from()
        recipients = self.get_recipients()
        subject = self.event.object.getMobile()
        message = self.expand_markers(self.element.message)

        email_charset = self.portal.getProperty('email_charset')
        for email_recipient in recipients:
            logger.debug('sending to: %s' % email_recipient)
            try:  # sending mail in Plone 4
                mailhost.send(message, mto=email_recipient, mfrom=source,
                              subject=subject, charset=email_charset)
            except:  # sending mail in Plone 3
                mailhost.secureSend(message, email_recipient, source,
                                    subject=subject, subtype='plain',
                                    charset=email_charset, debug=False,
                                    From=source)
        return True


class SMSFromFieldAddForm(AddForm):

    """
    An add form for the sms action
    """
    form_fields = form.FormFields(ISMSFromFieldAction)
    label = _(u"Add sms from field action")
    description = _(u"A sms send action that take the mobile number "
                    u"from the content where the rule is activated.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = SMSFromFieldAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class SMSFromFieldEditForm(EditForm):

    """
    An edit form for the sms action
    """
    form_fields = form.FormFields(ISMSFromFieldAction)
    label = _(u"Add sms from field action")
    description = _(u"A sms send action that take the mobile number "
                    u"from the content where the rule is activated.")
    form_name = _(u"Configure element")
