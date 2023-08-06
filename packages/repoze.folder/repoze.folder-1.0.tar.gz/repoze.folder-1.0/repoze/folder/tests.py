import unittest
from zope.component.testing import PlacelessSetup

class FolderTests(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _getTargetClass(self):
        from repoze.folder import Folder
        return Folder

    def _makeOne(self, data=None):
        klass = self._getTargetClass()
        return klass(data)

    def test_klass_provides_IFolder(self):
        klass = self._getTargetClass()
        from zope.interface.verify import verifyClass
        from repoze.folder.interfaces import IFolder
        verifyClass(IFolder, klass)
        
    def test_inst_provides_IFolder(self):
        from zope.interface.verify import verifyObject
        from repoze.folder.interfaces import IFolder
        inst = self._makeOne()
        verifyObject(IFolder, inst)

    def _registerEventListener(self, listener, iface):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from zope.interface import Interface
        gsm.registerHandler(listener, (Interface, iface,))

    def test_keys(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(list(folder.keys()), ['a', 'b'])

    def test_keys_with_order(self):
        folder = self._makeOne({'a':1, 'b':2})
        folder.order = ['b', 'a']
        self.assertEqual(list(folder.keys()), ['b', 'a'])

    def test_keys_after_del_order(self):
        folder = self._makeOne({'a':1, 'b':2})
        folder.order = ['b', 'a']
        del folder.order
        self.assertEqual(list(folder.keys()), ['a', 'b'])

    def test__iter__(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(list(folder), ['a', 'b'])

    def test__iter___with_order(self):
        folder = self._makeOne({'a':1, 'b':2})
        folder.order = ['b', 'a']
        self.assertEqual(list(folder), ['b', 'a'])

    def test_values(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(list(folder.values()), [1, 2])

    def test_values_with_order(self):
        folder = self._makeOne({'a':1, 'b':2})
        folder.order = ['b', 'a']
        self.assertEqual(list(folder.values()), [2, 1])

    def test_items(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(list(folder.items()), [('a', 1), ('b', 2)])

    def test_items_with_order(self):
        folder = self._makeOne({'a':1, 'b':2})
        folder.order = ['b', 'a']
        self.assertEqual(list(folder.items()), [('b', 2), ('a', 1)])

    def test__len__(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(len(folder), 2)
        del folder['a']
        self.assertEqual(len(folder), 1)

    def test__len___num_objects_None(self):
        folder = self._makeOne({'a':1, 'b':2})
        folder._num_objects = None
        self.assertEqual(len(folder), 2)
        del folder['a']
        self.assertEqual(len(folder), 1)

    def test__contains__(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertTrue('a' in folder)
        self.assertFalse('c' in folder)

    def test___nonzero__(self):
        folder = self._makeOne()
        self.assertTrue(folder)

    def test___setitem__nonstring(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, None)
        
    def test___setitem__8bitstring(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, '\xff')

    def test___setitem__empty(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, '')

    def test___setitem__(self):
        from repoze.folder.interfaces import IObjectEvent
        from repoze.folder.interfaces import IObjectWillBeAddedEvent
        from repoze.folder.interfaces import IObjectAddedEvent
        events = []
        def listener(object, event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        folder = self._makeOne()
        self.assertEqual(folder._num_objects(), 0)
        folder['a'] = dummy
        self.assertEqual(folder._num_objects(), 1)
        self.assertEqual(len(events), 2)
        self.assertTrue(IObjectWillBeAddedEvent.providedBy(events[0]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.assertTrue(IObjectAddedEvent.providedBy(events[1]))
        self.assertEqual(events[1].object, dummy)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')
        self.assertEqual(folder['a'], dummy)

    def test_add_name_wrongtype(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.add, 1, 'foo')

    def test_add_name_empty(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.add, '', 'foo')

    def test_add_send_events(self):
        from repoze.folder.interfaces import IObjectEvent
        from repoze.folder.interfaces import IObjectWillBeAddedEvent
        from repoze.folder.interfaces import IObjectAddedEvent
        events = []
        def listener(object, event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        folder = self._makeOne()
        self.assertEqual(folder._num_objects(), 0)
        folder.add('a', dummy, send_events=True)
        self.assertEqual(folder._num_objects(), 1)
        self.assertEqual(len(events), 2)
        self.assertTrue(IObjectWillBeAddedEvent.providedBy(events[0]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.assertTrue(IObjectAddedEvent.providedBy(events[1]))
        self.assertEqual(events[1].object, dummy)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')
        self.assertEqual(folder['a'], dummy)

    def test_add_suppress_events(self):
        from repoze.folder.interfaces import IObjectEvent
        events = []
        def listener(object, event):
            events.append(event) #pragma NO COVER
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        folder = self._makeOne()
        self.assertEqual(folder._num_objects(), 0)
        folder.add('a', dummy, send_events=False)
        self.assertEqual(folder._num_objects(), 1)
        self.assertEqual(len(events), 0)
        self.assertEqual(folder['a'], dummy)

    def test_add_with_order_appends_name(self):
        folder = self._makeOne()
        folder.order = []
        folder.add('a', DummyModel())
        self.assertEqual(folder.order, ['a'])
        folder.add('b', DummyModel())
        self.assertEqual(folder.order, ['a', 'b'])

    def test___setitem__exists(self):
        dummy = DummyModel()
        folder = self._makeOne({'a':dummy})
        self.assertEqual(folder._num_objects(), 1)
        self.assertRaises(KeyError, folder.__setitem__, 'a', dummy)
        self.assertEqual(folder._num_objects(), 1)

    def test___delitem__(self):
        from repoze.folder.interfaces import IObjectEvent
        from repoze.folder.interfaces import IObjectRemovedEvent
        from repoze.folder.interfaces import IObjectWillBeRemovedEvent
        events = []
        def listener(object, event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        dummy.__parent__ = None
        dummy.__name__ = None
        folder = self._makeOne({'a':dummy})
        self.assertEqual(folder._num_objects(), 1)
        del folder['a']
        self.assertEqual(folder._num_objects(), 0)
        self.assertEqual(len(events), 2)
        self.assertTrue(IObjectWillBeRemovedEvent.providedBy(events[0]))
        self.assertTrue(IObjectRemovedEvent.providedBy(events[1]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.assertEqual(events[1].object, dummy)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')
        self.assertFalse(hasattr(dummy, '__parent__'))
        self.assertFalse(hasattr(dummy, '__name__'))

    def test_remove_miss(self):
        folder = self._makeOne()
        self.assertRaises(KeyError, folder.remove, "nonesuch")

    def test_remove_returns_object(self):
        dummy = DummyModel()
        dummy.__parent__ = None
        dummy.__name__ = None
        folder = self._makeOne({'a':dummy})
        self.assertTrue(folder.remove("a") is dummy)

    def test_remove_send_events(self):
        from repoze.folder.interfaces import IObjectEvent
        from repoze.folder.interfaces import IObjectRemovedEvent
        from repoze.folder.interfaces import IObjectWillBeRemovedEvent
        events = []
        def listener(object, event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        dummy.__parent__ = None
        dummy.__name__ = None
        folder = self._makeOne({'a':dummy})
        self.assertEqual(folder._num_objects(), 1)
        folder.remove('a', send_events=True)
        self.assertEqual(folder._num_objects(), 0)
        self.assertEqual(len(events), 2)
        self.assertTrue(IObjectWillBeRemovedEvent.providedBy(events[0]))
        self.assertTrue(IObjectRemovedEvent.providedBy(events[1]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.assertEqual(events[1].object, dummy)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')
        self.assertFalse(hasattr(dummy, '__parent__'))
        self.assertFalse(hasattr(dummy, '__name__'))

    def test_remove_suppress_events(self):
        from repoze.folder.interfaces import IObjectEvent
        events = []
        def listener(object, event):
            events.append(event) #pragma NO COVER
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        dummy.__parent__ = None
        dummy.__name__ = None
        folder = self._makeOne({'a':dummy})
        self.assertEqual(folder._num_objects(), 1)
        folder.remove('a', send_events=False)
        self.assertEqual(folder._num_objects(), 0)
        self.assertEqual(len(events), 0)
        self.assertFalse(hasattr(dummy, '__parent__'))
        self.assertFalse(hasattr(dummy, '__name__'))

    def test_remove_with_order_removes_name(self):
        folder = self._makeOne()
        folder['a'] = DummyModel()
        folder['b'] = DummyModel()
        folder.order = ['a', 'b']
        folder.remove('a')
        self.assertEqual(folder.order, ['b'])

    def test_pop_success(self):
        from repoze.folder.interfaces import IObjectEvent
        from repoze.folder.interfaces import IObjectRemovedEvent
        from repoze.folder.interfaces import IObjectWillBeRemovedEvent
        dummy = DummyModel()
        dummy.__parent__ = None
        dummy.__name__ = None
        events = []
        def listener(object, event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        folder = self._makeOne({'a':dummy})
        result = folder.pop('a')
        self.assertEqual(result, dummy)
        self.assertEqual(folder._num_objects(), 0)
        self.assertEqual(len(events), 2)
        self.assertTrue(IObjectWillBeRemovedEvent.providedBy(events[0]))
        self.assertTrue(IObjectRemovedEvent.providedBy(events[1]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.assertEqual(events[1].object, dummy)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')
        self.assertFalse(hasattr(dummy, '__parent__'))
        self.assertFalse(hasattr(dummy, '__name__'))

    def test_pop_fail_nodefault(self):
        folder = self._makeOne()
        self.assertRaises(KeyError, folder.pop, 'nonesuch')

    def test_pop_fail_withdefault(self):
        folder = self._makeOne()
        result = folder.pop('a', 123)
        self.assertEqual(result, 123)

    def test_repr(self):
        folder = self._makeOne()
        folder.__name__ = 'thefolder'
        r = repr(folder)
        self.assertTrue(
            "<repoze.folder.Folder object 'thefolder' at " in r)
        self.assertTrue(r.endswith('>'))

    def test_str(self):
        folder = self._makeOne()
        folder.__name__ = 'thefolder'
        r = str(folder)
        self.assertTrue(
            "<repoze.folder.Folder object 'thefolder' at " in r)
        self.assertTrue(r.endswith('>'))

    def test_unresolveable_unicode_setitem(self):
        from repoze.folder._compat import text_
        name = text_(b'La Pe\xc3\xb1a', 'utf-8').encode('latin-1')
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, name, DummyModel())

    def test_resolveable_unicode_setitem(self):
        name = 'La Pe\xc3\xb1a'
        folder = self._makeOne()
        folder[name] = DummyModel()
        self.assertTrue(folder.get(name))

    def test_unresolveable_unicode_getitem(self):
        from repoze.folder._compat import text_
        name = text_(b'La Pe\xc3\xb1a', 'utf-8').encode('latin-1')
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__getitem__, name)

    def test_resolveable_unicode_getitem(self):
        name = 'La Pe\xc3\xb1a'
        folder = self._makeOne()
        folder[name] = DummyModel()
        self.assertTrue(folder[name])

    def test_bwcompat_nolength_delitem(self):
        folder = self._makeOne()
        folder['a'] = DummyModel()
        folder['b'] = DummyModel()
        self.assertEqual(folder._num_objects(), 2)
        folder._num_objects = None
        del folder['a']
        self.assertEqual(folder._num_objects(), 1)

    def test_bwcompat_nolength_setitem(self):
        folder = self._makeOne()
        folder['a'] = DummyModel()
        folder['b'] = DummyModel()
        self.assertEqual(folder._num_objects(), 2)
        folder._num_objects = None
        folder['c'] = DummyModel()
        self.assertEqual(folder._num_objects(), 3)


class UnicodifyTests(unittest.TestCase):
    def _callFUT(self, name, sysencoding=None):
        from repoze.folder import unicodify
        return unicodify(name, sysencoding)

    def test_default_encoding_works(self):
        from repoze.folder._compat import text_
        result = self._callFUT('abc')
        self.assertEqual(result, text_(b'abc'))

    def test_utf8_encoding_works(self):
        from repoze.folder._compat import text_
        result = self._callFUT(b'La Pe\xc3\xb1a')
        self.assertEqual(result, text_(b'La Pe\xc3\xb1a', 'utf-8'))

    def test_unicode_works(self):
        from repoze.folder._compat import text_
        result = self._callFUT(text_(b'La Pe\xc3\xb1a', 'utf-8'))
        self.assertEqual(result, text_(b'La Pe\xc3\xb1a', 'utf-8'))
        
    def test_unknown_encoding_breaks(self):
        from repoze.folder._compat import text_
        name = text_(b'La Pe\xc3\xb1a', 'utf-8').encode('utf-16')
        self.assertRaises(TypeError, self._callFUT, name)

    def test_sysencoding_utf8(self):
        from repoze.folder._compat import text_
        name = text_(b'La Pe\xc3\xb1a', 'utf-8').encode('utf-16')
        self.assertRaises(TypeError, self._callFUT, name, 'utf-8')

class DummyModel:
    pass

