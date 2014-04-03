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

from redomino.advancedkeyword import MessageFactory as _

class IAdvancedKeyword(form.Schema):
    """Add tags to content
    """

    form.fieldset(
            'categorization',
            label=_(u'Categorization'),
            fields=('tags',),
        )

    tags = schema.TextLine(title=u"Tags lala")
    #
    # tags = schema.TextLine(
    #         title=_(u"Subject"),
    #         description=_(u"Applicable tags"),
    #         required=False,
    #         # allow_uncommon=True,
    #     )

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
    def tags(self):
        return set(self.context.Subject())
    @setproperty
    def tags(self, value):
        if value is None:
            value = ()
        self.context.setSubject(tuple(value))