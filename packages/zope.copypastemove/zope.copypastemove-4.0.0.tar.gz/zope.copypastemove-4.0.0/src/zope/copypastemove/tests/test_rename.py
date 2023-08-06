##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test renaming of components
"""
import doctest
import re
import unittest

from zope.component import testing, eventtesting, provideAdapter, adapter
from zope.container.testing import PlacelessSetup, ContainerPlacefulSetup
from zope.copypastemove import ContainerItemRenamer, ObjectMover
from zope.copypastemove.interfaces import IContainerItemRenamer
from zope.container.contained import Contained, NameChooser
from zope.container.sample import SampleContainer
from zope.testing import renormalizing

checker = renormalizing.RENormalizing([
    # Python 3 unicode removed the "u".
    (re.compile("u('.*?')"),
     r"\1"),
    (re.compile('u(".*?")'),
     r"\1"),
    ])

class TestContainer(SampleContainer):
    pass

@adapter(TestContainer)
class ObstinateNameChooser(NameChooser):

    def chooseName(self, name, ob):
        return u'foobar'

class RenamerTest(ContainerPlacefulSetup, unittest.TestCase):

    def setUp(self):
        ContainerPlacefulSetup.setUp(self)
        provideAdapter(ObjectMover)
        provideAdapter(ContainerItemRenamer)
        provideAdapter(ObstinateNameChooser)

    def test_obstinatenamechooser(self):
        container = TestContainer()
        container[u'foobar'] = Contained()
        renamer = IContainerItemRenamer(container)

        renamer.renameItem(u'foobar', u'newname')
        self.assertEqual(list(container), [u'foobar'])

container_setup = PlacelessSetup()

def setUp(test):
    testing.setUp()
    eventtesting.setUp()
    container_setup.setUp()


def doctest_namechooser_rename_preserve_order():
    """Test for OrderedContainerItemRenamer.renameItem

    This is a regression test for
    http://www.zope.org/Collectors/Zope3-dev/658

    Also: https://bugs.launchpad.net/zope.copypastemove/+bug/98385

        >>> from zope.component import adapter, provideAdapter
        >>> from zope.copypastemove import ObjectMover
        >>> provideAdapter(ObjectMover)

    There's an ordered container

        >>> from zope.container.ordered import OrderedContainer
        >>> container = OrderedContainer()

        >>> from zope.container.contained import Contained
        >>> class Obj(Contained):
        ...     def __init__(self, title):
        ...         self.title = title
        ...     def __repr__(self):
        ...         return self.title
        >>> container['foo'] = Obj('Foo')
        >>> container['bar'] = Obj('Bar')
        >>> container['baz'] = Obj('Baz')

    with a custom name chooser

        >>> import codecs
        >>> from zope.interface import implementer, Interface
        >>> from zope.container.interfaces import INameChooser
        >>> class IMyContainer(Interface): pass
        >>> @adapter(IMyContainer)
        ... @implementer(INameChooser)
        ... class MyNameChooser(object):
        ...     def __init__(self, container):
        ...         self.container = container
        ...     def chooseName(self, name, obj):
        ...         return codecs.getencoder('rot-13')(name)[0]
        >>> provideAdapter(MyNameChooser)

        >>> from zope.interface import alsoProvides
        >>> alsoProvides(container, IMyContainer)

    OrderedContainerItemRenamer renames and preserves the order of items

        >>> from zope.copypastemove import OrderedContainerItemRenamer
        >>> renamer = OrderedContainerItemRenamer(container)
        >>> renamer.renameItem('bar', 'quux')
        'dhhk'

        >>> list(container.keys())
        ['foo', 'dhhk', 'baz']
        >>> list(container.values())
        [Foo, Bar, Baz]

    """

def test_suite():
    flags = \
        doctest.NORMALIZE_WHITESPACE | \
        doctest.ELLIPSIS | \
        doctest.IGNORE_EXCEPTION_DETAIL
    return unittest.TestSuite((
            unittest.makeSuite(RenamerTest),
            doctest.DocTestSuite('zope.copypastemove',
                         setUp=setUp, tearDown=testing.tearDown,
                         checker=checker, optionflags=flags),
            doctest.DocTestSuite(setUp=setUp, tearDown=testing.tearDown),
            ))
