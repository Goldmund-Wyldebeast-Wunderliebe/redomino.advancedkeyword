"""Behaviours to assign tags (to ideas).

Includes a form field and a behaviour adapter that stores the data in the
standard Subject field.
"""
from rwproperty import getproperty, setproperty
from z3c.form.browser.select import SelectWidget
from zope import schema

from zope.interface import implements, alsoProvides
from zope.component import adapts

from plone.directives import form

from Products.CMFCore.interfaces import IDublinCore

# from collective.z3cform.keywordwidget.field import Keywords

from redomino.advancedkeyword import _
from redomino.advancedkeyword.behavior.field import AdvancedKeyword
from redomino.advancedkeyword.behavior.widget import AdvancedKeywordWidget
from redomino.advancedkeyword import PloneMessageFactory as _PMF

import logging
logger = logging.getLogger(__name__)

class IAdvancedKeyword(form.Schema):
    """Add tags to content
    """

    form.fieldset(
        'categorization',
        label=_PMF(u'label_schema_categorization', default=u'Categorization'),
        fields=('advanced_keyword',),
    )

    form.widget('advanced_keyword', AdvancedKeywordWidget)
    advanced_keyword = AdvancedKeyword(
        title=_PMF(u'label_tags', default=u'Tags'),
        description=_PMF(
            u'help_tags',
            default=u'Tags are commonly used for ad-hoc organization of ' +
                    u'content.'
        ),
        required=False,
    )

alsoProvides(IAdvancedKeyword, form.IFormFieldProvider)

class AdvancedKeyword(object):
    """Store tags in the Dublin Core metadata Subject field. This makes
    tags easy to search for.
    """
    implements(IAdvancedKeyword)
    # adapts(IDublinCore)
    adapts(IDublinCore)

    def __init__(self, context):
        self.context = context

    @getproperty
    def advanced_keyword(self):
        logger.info('get: {0}'.format(self.context.Subject()))
        return set(self.context.Subject())

    @setproperty
    def advanced_keyword(self, value):
        if value is None:
            value = ()

        logger.info('set: {0}'.format(value))
        self.context.setSubject(tuple(value))