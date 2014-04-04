from z3c.form.converter import BaseDataConverter
from zope import schema
from zope.component import adapts
from zope.interface import implements
from redomino.advancedkeyword.behavior.interfaces import IAdvancedKeywordCollection, IAdvancedKeywordWidget

import logging
logger = logging.getLogger(__name__)


class AdvancedKeyword(schema.List):
    """A field representing a set."""
    implements(IAdvancedKeywordCollection)
    unique = True
    index_name = None

    def __init__(self, value_type=None, unique=False, index_name=None, **kw):
        super(AdvancedKeyword, self).__init__(value_type=value_type, unique=unique, **kw)
        if not value_type:
            self.value_type = schema.TextLine()

        self.index_name = index_name


class KeywordsDataConverter(BaseDataConverter):
    """A special converter between collections and sequence widgets."""

    adapts(IAdvancedKeywordCollection, IAdvancedKeywordWidget)

    def toWidgetValue(self, value):
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]

        if value:
            return collectionType(value)
        else:
            return collectionType()

    def toFieldValue(self, value):
        """See interfaces.IDataConverter
        """
        widget = self.widget
        if widget.terms is None:
            widget.updateTerms()
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]

        logger.info(value)
        return collectionType(value)
