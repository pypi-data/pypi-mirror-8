# -*- coding: utf-8 -*-

import unittest

from zope.component import getMultiAdapter

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login

from collective.tablepage.interfaces import IDataStorage
from collective.tablepage.testing import TABLE_PAGE_INTEGRATION_TESTING


class LinkFieldTestCase(unittest.TestCase):

    layer = TABLE_PAGE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        wtool = portal.portal_workflow
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='TablePage', id='table_page', title="The Table Document")
        portal.invokeFactory(type_name='Document', id='document', title="A d\xc3\xb2cument to reference",
                             description="Hello docum\xc3\xa8nt!")
        tp = portal.table_page
        tp.edit(pageColumns=[{'id': 'link', 'label': 'Link', 'description': '',
                              'type': 'Link', 'vocabulary': '', 'options': []}])
        wtool.doActionFor(tp, 'publish')

    def test_reference_document_edit(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        storage = IDataStorage(tp)
        storage.add({'__creator__': TEST_USER_NAME, 'link': portal.document.UID(),
                     '__uuid__': 'aaa'})
        request.form['row-index'] = 0
        view = getMultiAdapter((tp, request), name=u'edit-record')
        self.assertTrue('value="%s"' % portal.document.Title().decode('utf-8') in view())

    def test_url_edit(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        storage = IDataStorage(tp)
        storage.add({'__creator__': TEST_USER_NAME, 'link': 'http://foo.com/',
                     '__uuid__': 'aaa'})
        request.form['row-index'] = 0
        view = getMultiAdapter((tp, request), name=u'edit-record')
        self.assertTrue('http://foo.com/' in view())

    def test_noturl_edit(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        storage = IDataStorage(tp)
        storage.add({'__creator__': TEST_USER_NAME, 'link': 'foo bar baz',
                     '__uuid__': 'aaa'})
        request.form['row-index'] = 0
        view = getMultiAdapter((tp, request), name=u'edit-record')
        self.assertTrue('foo bar baz' not in view())
        self.assertTrue('value="%s"' % portal.document.Title().decode('utf-8') not in view())

    def test_url_save(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        request.form['external_link'] = 'http://mycompany.com/'
        request.form['form.submitted'] = '1'
        view = getMultiAdapter((tp, request), name=u'edit-record')
        view()
        storage = IDataStorage(tp)
        self.assertEqual(storage[0]['link'], 'http://mycompany.com/')

    def test_delete_old_data(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        storage = IDataStorage(tp)
        storage.add({'__creator__': TEST_USER_NAME, 'link': portal.document.UID(),
                     '__uuid__': 'aaa'})
        request.form['row-index'] = 0
        request.form['form.submitted'] = '1'
        request.form['external_link'] = ''
        request.form['internal_link'] = ''
        view = getMultiAdapter((tp, request), name=u'edit-record')
        view()
        self.assertFalse(storage[0]['link']==portal.document.UID())
        self.assertEqual(storage[0]['link'], '')

    def test_reference_save(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        request.form['internal_link'] = portal.document.UID()
        request.form['form.submitted'] = '1'
        view = getMultiAdapter((tp, request), name=u'edit-record')
        view()
        storage = IDataStorage(tp)
        self.assertEqual(storage[0]['link'], portal.document.UID())

    def test_reference_internal_ref_precedence(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        request.form['external_link'] = 'http://mycompany.com/'
        request.form['internal_link'] = portal.document.UID()
        request.form['form.submitted'] = '1'
        view = getMultiAdapter((tp, request), name=u'edit-record')
        view()
        storage = IDataStorage(tp)
        self.assertEqual(storage[0]['link'], portal.document.UID())

    def test_foo_data_saved_however(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        request.form['external_link'] = 'this is not an url'
        request.form['internal_link'] = 'this is not an uid'
        request.form['form.submitted'] = '1'
        view = getMultiAdapter((tp, request), name=u'edit-record')
        view()
        storage = IDataStorage(tp)
        self.assertEqual(storage[0]['link'], 'this is not an uid')
        output = tp()
        self.assertFalse('this is not an uid' in output)

    def test_template_override_text(self):
        portal = self.layer['portal']
        tp = portal.table_page
        tp.edit(pageColumns=[{'id': 'link', 'label': 'Link', 'description': '',
                              'type': 'Link', 'vocabulary': 'title:Lorèm ipsum', 'options': []}])
        storage = IDataStorage(tp)
        storage.add({'__creator__': TEST_USER_NAME, 'link': portal.document.UID(),
                     '__uuid__': 'aaa'})
        output = tp()
        self.assertTrue(u'Lor\xe8m ipsum' in output)

    def test_template_override_icon(self):
        portal = self.layer['portal']
        tp = portal.table_page
        tp.edit(pageColumns=[{'id': 'link', 'label': 'Link', 'description': '',
                              'type': 'Link', 'vocabulary': 'icon:src-to-an-icon', 'options': []}])
        storage = IDataStorage(tp)
        storage.add({'__creator__': TEST_USER_NAME, 'link': portal.document.UID(),
                     '__uuid__': 'aaa'})
        output = tp()
        self.assertTrue(u'<img src="src-to-an-icon" alt="A d\xf2cument to reference" />' in output)
