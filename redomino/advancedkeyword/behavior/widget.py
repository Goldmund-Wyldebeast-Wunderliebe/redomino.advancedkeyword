from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from plone.i18n.normalizer import IIDNormalizer
from z3c.form.i18n import MessageFactory as _
from z3c.form import interfaces as z3cfinterfaces
from z3c.form.browser.select import SelectWidget
from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.term import Terms
from z3c.form.widget import FieldWidget

from zope.component import getUtility, adapter

from zope.interface import implementsOnly, implementer
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from redomino.advancedkeyword.behavior.interfaces import IAdvancedKeywordWidget, IAdvancedKeywordCollection

from redomino.advancedkeyword.browser.utils import get_keywords

import logging
logger = logging.getLogger(__name__)


class AdvancedKeywordWidget(SelectWidget):

    implementsOnly(IAdvancedKeywordWidget)
    klass = u'advanced-keyword-widget'
    multiple = 'multiple'
    size = 14
    noValueToken = u''
    noValueMessage = _('no value')
    promptMessage = _('select a value ...')
    roleBasedAdd = True

    @property
    def formatted_value(self):
        if not self.value:
            return ''
        return '<br/>'.join(self.value)

    def getValuesFromRequest(self, default=z3cfinterfaces.NOVALUE):
        """Get the values from the request and split the terms with newlines
        """
        new_val = []
        old_val = self.request.get(self.name, [])
        for v in self.request.get('%s_additional' % self.name, "").split("\n"):
            clean = v.strip().strip("\r").strip("\n")
            if clean and clean not in old_val:
                new_val.append(clean)
        return old_val + new_val

    def isSelected(self, term):
        return term.title in self.value

    def extract(self, default=z3cfinterfaces.NOVALUE):
        """See z3c.form.interfaces.IWidget.
        """
        if (self.name not in self.request and
            self.name + '_additional' not in self.request and
            self.name + '-empty-marker' in self.request):
            return default

        value = self.getValuesFromRequest() or default
        titles = []
        normalizer = getUtility(IIDNormalizer)

        if value != default:
            for val in value:
                token = normalizer.normalize(val)
                if token == self.noValueToken:
                    continue

                try:
                    term = self.terms.getTermByToken(token)
                    titles.append(term.title)
                except LookupError:
                    # a new value is entered which is not available in vocab
                    continue
        logger.debug(titles)
        return len(titles) > 0 and tuple(titles) or default

    def updateTerms(self):
        if self.terms is None:
            self.terms = Terms()

        values = get_keywords()

        if None in values or '' in values:
            values = [v for v in values if v]

        added_values = self.getValuesFromRequest()
        for value in added_values:
            if value and value not in values:
                values.append(value)

        items = []
        unique_values = set()
        normalizer = getUtility(IIDNormalizer)

        for value in values:
            token = normalizer.normalize(value)
            if token not in unique_values:
                unique_values.add(token)
                items.append(SimpleTerm(value, token, safe_unicode(value)))

        self.terms.terms = SimpleVocabulary(items)
        return self.terms

    @property
    def generator(self):
        return self.context.restrictedTraverse('keywordswidgetgenerator')

    def show_new_kw(self):

        if not self.roleBasedAdd:
            return True
        elif self.items:
            portal_membership = getToolByName(self.context, 'portal_membership')
            portal_properties = getToolByName(self.context, 'portal_properties')

            member = portal_membership.getAuthenticatedMember()
            allowRolesToAddKeywords = portal_properties.site_properties.allowRolesToAddKeywords

            for role in member.getRolesInContext(self.context):
                if role in allowRolesToAddKeywords:
                    return True


@adapter(IAdvancedKeywordCollection,
         IFormLayer)
@implementer(IFieldWidget)
def AdvancedKeywordFieldWidget(field, request):
    """ IFieldWidget factory for KeywordWidget
    """
    return FieldWidget(field, AdvancedKeywordWidget(request))
