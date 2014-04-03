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
import os
from z3c.form.interfaces import IFormLayer
from z3c.form.term import Terms
from zope.component import provideAdapter

from zope.interface.verify import verifyClass
from z3c.form.testing import TestRequest
from zope.schema.vocabulary import SimpleVocabulary
from redomino.advancedkeyword.behavior.widget import IKeywordWidget, KeywordWidget

from redomino.advancedkeyword.tests.base import TestCase

BEHAVIOR = 'redomino.advancedkeyword.behavior.behavior.IAdvancedKeyword'


class TestWidget(TestCase):
    """ Test the z3c.form keyword widget used by the Dexterity behavior
    """

    def afterSetUp(self):
        self.request = TestRequest()

    def _setupWidget(self):
        widget = KeywordWidget(self.request)
        widget.id = 'widget-id'
        widget.name = 'widget.name'
        # widget needs context to traverse keywordswidgetgenerator
        widget.context = self.portal
        return widget

    def test_interface(self):
        self.assertTrue(verifyClass(IKeywordWidget, KeywordWidget))

    def test_empty(self):
        widget = self._setupWidget()
        html = widget.render()
        self.assertIsNotNone(html)

    def test_terms(self):
        widget = self._setupWidget()

        class SelectionTerms(Terms):
            def __init__(self, context, request, form, field, widget):
                self.terms = SimpleVocabulary.fromValues(['spam', 'bacon', 'eggs'])

        provideAdapter(SelectionTerms,
             (None, IFormLayer, None, None, IKeywordWidget) )

        widget.update()
        html = widget.render()

        self.assertIn(
            '<option id="widget-id-1" value="bacon">bacon</option>', html
        )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWidget))
    return suite


