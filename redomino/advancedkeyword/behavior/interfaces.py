from z3c.form.interfaces import ISequenceWidget
from zope import schema


class IAdvancedKeywordWidget(ISequenceWidget):
    """A keyword widget.
    """

class IAdvancedKeywordCollection(schema.interfaces.ICollection):
    """ Marker interfaces for keyword collections
    """

    index_name = schema.TextLine(title=u"Index name",
                                 description=u"Name of the catalog index "
                                             u"for the values of this field")