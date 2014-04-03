"""Behaviours to assign tags (to ideas).

Includes a form field and a behaviour adapter that stores the data in the
standard Subject field.
"""
from rwproperty import getproperty, setproperty
from zope import schema

from zope.interface import implements, alsoProvides
from zope.component import adapts

from plone.directives import form

from Products.CMFCore.interfaces import IDublinCore

from redomino.advancedkeyword import _
from redomino.advancedkeyword.behavior.widget import KeywordWidget


class IAdvancedKeyword(form.Schema):
    """Add tags to content
    """

    form.fieldset(
            'categorization',
            label=_(u'Categorization'),
            fields=('advanced_keyword',),
        )

    form.widget('advanced_keyword', KeywordWidget)
    advanced_keyword = schema.Set(
        title=_(u'Tags'),
        description=_(
            u'Tags are commonly used for ad-hoc organization of content.'
        ),
        value_type=schema.Choice(
            vocabulary=u"plone.app.vocabularies.Keywords",
        ),
        required=False,
        missing_value=(),
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
        return set(self.context.Subject())

    @setproperty
    def advanced_keyword(self, value):
        if value is None:
            value = ()
        self.context.setSubject(tuple(value))