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

import unittest2 as unittest
from plone.dexterity.fti import DexterityFTI

from redomino.advancedkeyword.tests.base import TestCase

class TestBehavior(TestCase):
    """ Check if js, css, etc are correctly registered
    """

    def afterSetUp(self):
        self.setRoles(('Manager', ))

        # Create a dummy Dexterity container to work with
        fti = DexterityFTI('Container')
        self.portal.portal_types._setObject('Container', fti)
        fti.klass = 'plone.dexterity.content.Container'
        fti.behaviors = ('redomino.advancedkeyword.behavior.IAdvancedKeyword',)
        fti.allowed_content_types = ('Folder',)

        # Default configuration for container
        id = self.portal.invokeFactory('Container', 'container')
        self.container = self.portal[id]

    def test_container(self):
        self.assertEqual(self.container.id, 'container')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBehavior))
    return suite


