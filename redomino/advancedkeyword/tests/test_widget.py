# Copyright (c) 2011 Redomino srl (http://redomino.com)
# Authors: Davide Moro <davide.moro@redomino.com> and contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# TODO: make sure this test does not break when DX is not used.
from OFS.SimpleItem import SimpleItem
from z3c.form import field
from z3c.form.form import AddForm, EditForm
from zope import schema
from zope import interface
from zope.interface import alsoProvides

from zope.interface.verify import verifyClass
from z3c.form.testing import TestRequest, lxml
from zope.schema.fieldproperty import FieldProperty
from redomino.advancedkeyword.behavior.field import AdvancedKeyword

from redomino.advancedkeyword.behavior.widget import IAdvancedKeywordWidget, AdvancedKeywordWidget, \
    AdvancedKeywordFieldWidget
from redomino.advancedkeyword.tests.base import TestCase

BEHAVIOR = 'redomino.advancedkeyword.behavior.behavior.IAdvancedKeyword'


class IFoo(interface.Interface):
    id = schema.TextLine(
        title=u'ID',
        readonly=True,
        required=True
    )
    keywords = AdvancedKeyword(
        title=u'Keywords',
        required=True
    )


class Foo(SimpleItem):
    interface.implements(IFoo)
    id = FieldProperty(IFoo['id'])
    keywords = FieldProperty(IFoo['keywords'])

    def __init__(self, id, keywords):
        super(Foo, self).__init__(id)
        self.id = id
        self.keywords = keywords
        

class FooAddForm(AddForm):
    fields = field.Fields(IFoo)
    fields['keywords'].widgetFactory = AdvancedKeywordFieldWidget

    def create(self, data):
        return Foo(**data)

    def add(self, contentobj):
        self.context[str(contentobj.id)] = contentobj

    def nextURL(self):
        return 'index.html'


class FooEditForm(EditForm):
    fields = field.Fields(IFoo)
    fields['keywords'].widgetFactory = AdvancedKeywordFieldWidget


class TestWidget(TestCase):
    """ Test the z3c.form keyword widget used by the Dexterity behavior
    """

    def afterSetUp(self):
        self.request = TestRequest()
        self.setRoles(('Manager', ))
        self.catalog = self.portal.portal_catalog
        
        alsoProvides(self.portal, IFoo)
        
    def _setupWidget(self):
        widget = AdvancedKeywordWidget(self.request)
        widget.id = 'widget-id'
        widget.name = 'widget.name'
        # widget needs context to traverse keywordswidgetgenerator
        widget.context = self.portal
        return widget

    def test_interface(self):
        self.assertTrue(verifyClass(IAdvancedKeywordWidget, AdvancedKeywordWidget))

    def test_empty(self):
        widget = self._setupWidget()
        html = widget.render()
        self.assertIsNotNone(html)

    def test_form_empty(self):
        """ Render the field/widget in an empty form """
        request = TestRequest()

        addForm = FooAddForm(self.portal, request)
        addForm.update()

        # Check for the keyword widget and render it
        self.assertEqual(
            addForm.widgets.keys(),
            ['id', 'keywords']
        )
        html = addForm.widgets['keywords'].render()

        # There is a field to input new keywords
        self.assertIn(
            '<div id="advancedNewTagsSection" style=" ">',
            html
        )
        # There are no existing tags
        self.assertNotIn(
            '<div id="advancedExistingTagsSection">',
            html
        )

    def test_form_save_keywords(self):
        """ Try to save keywords using the field/widget """

        request = TestRequest(form={
            'form.widgets.id': u'myobject',
            'form.widgets.keywords_additional': u'python.spam\npython.bacon\npython.eggs',
            'form.buttons.add': u'Add'}
        )

        addForm = FooAddForm(self.portal, request)
        addForm.update()

        self.assertEqual(addForm.status, '')

        myobject = self.portal['myobject']
        self.assertEqual(myobject.__class__, Foo)

        # The keywords are stores in the object
        self.assertEqual(
            myobject.keywords,
            [u'python.spam', u'python.bacon', u'python.eggs']
        )

    def test_form_with_keywords(self):
        """ View existing keywords with field/widget """

        keywords = ('python', 'python.bacon', 'python.eggs', 'python.spam')

        # Manually add keywords to front-page document
        self.portal['front-page'].setSubject(keywords)
        self.catalog.clearFindAndRebuild()

        # The catalog contains the keywords
        self.assertEqual(
            self.catalog.uniqueValuesFor('Subject'), keywords
        )

        request = TestRequest()

        addForm = FooAddForm(self.portal, request)
        addForm.update()

        html = addForm.widgets['keywords'].render()

        lxml_tree = lxml.html.document_fromstring(html)


        # Get elements for subject tree
        tree = lxml_tree.find_class('subjectTree')
        self.assertEqual(len(tree), 1)
        tree = lxml.html.tostring(tree[0])

        # Get elements for hidden keyword field
        widget = lxml_tree.get_element_by_id('form-widgets-keywords')
        self.assertIsNotNone(widget)
        widget = lxml.html.tostring(widget)

        for idx, kw in enumerate(keywords):
            token = kw.replace('.', '-')

            # Check for subject tree
            self.assertIn(
                'id="{0}" value="{1}"'.format(token, kw), tree
            )
            # Check for hidden keyword widget
            self.assertIn(
                'value="{0}">{1}</option>'.format(token, kw), widget
            )


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWidget))
    return suite


