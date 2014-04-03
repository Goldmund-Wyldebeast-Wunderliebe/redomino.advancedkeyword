from Products.CMFPlone.utils import safe_unicode
from unicodedata import normalize
from z3c.form.i18n import MessageFactory as _
import re
from z3c.form import interfaces as z3cfinterfaces
from z3c.form.browser.select import SelectWidget
import z3c.form

import zope.component
import zope.interface


class IKeywordWidget(z3c.form.interfaces.ISequenceWidget):
    """A keyword widget.
    """


class KeywordWidget(SelectWidget):

    zope.interface.implementsOnly(IKeywordWidget)
    klass = u'advanced-keyword-widget'
    multiple = 'multiple'
    size = 14
    noValueToken = u''
    noValueMessage = _('no value')
    promptMessage = _('select a value ...')

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
        if value == default:
            return default

        extracted = set()
        for token in value:
            if token == self.noValueToken:
                extracted.append(value)
            elif token:
                extracted.add(token)

        return extracted

    @property
    def generator(self):
        return self.context.restrictedTraverse('keywordswidgetgenerator')
