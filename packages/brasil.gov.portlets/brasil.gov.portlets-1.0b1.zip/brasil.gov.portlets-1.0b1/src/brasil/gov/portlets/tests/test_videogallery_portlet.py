# -*- coding: utf-8 -*-
from Products.GenericSetup.utils import _getDottedName
from brasil.gov.portlets.portlets import videogallery
from brasil.gov.portlets.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from zope.component import getMultiAdapter
from zope.component import getUtility


import unittest


class VideoGalleryPortletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.videos = {}
        self.videos['collection'] = self.portal['videos-folder']['videos-collection']
        self.videos['path'] = '/' + '/'.join(self.videos['collection'].getPhysicalPath()[2:])
        self.videos['url'] = self.videos['collection'].absolute_url()

        self.files = {}
        self.files['collection'] = self.portal['files-folder']['files-collection']
        self.files['path'] = '/' + '/'.join(self.files['collection'].getPhysicalPath()[2:])
        self.files['url'] = self.files['collection'].absolute_url()

    def _renderer(self, context=None, request=None, view=None, manager=None,
                  assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def _assigned_renderer(self, col):
        assgmnt = videogallery.Assignment(
            show_header=True,
            header=u'Portal Padrão Galeria de Vídeos',
            header_type=u'H2',
            show_active_title=True,
            show_inactive_title=True,
            show_description=True,
            show_footer=True,
            footer=u'Mais...',
            footer_url=col['url'],
            limit=3,
            collection=col['path']
        )
        r = self._renderer(context=self.portal,
                           assignment=assgmnt)
        r = r.__of__(self.portal)
        r.update()
        return r

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.videogallery')
        self.assertEqual(portlet.addview, 'brasil.gov.portlets.videogallery')

    def test_registered_interfaces(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.videogallery')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEqual(
            ['plone.app.portlets.interfaces.IColumn',
             'plone.app.portlets.interfaces.IDashboard'],
            registered_interfaces
        )

    def test_interfaces(self):
        portlet = videogallery.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_addview(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.videogallery')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], videogallery.Assignment))

    def test_portlet_properties(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.videogallery')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={
            'show_header': True,
            'header': u'Portal Padrão Galeria de Vídeos',
            'header_type': u'H4',
            'show_active_title': True,
            'show_inactive_title': True,
            'show_description': True,
            'show_footer': True,
            'footer': u'Mais...',
            'footer_url': self.videos['url'],
            'limit': 2,
            'collection': self.videos['path']
        })

        title = mapping.values()[0].title
        self.assertEqual(title, u'Portal Padrão Galeria de Vídeos')

        header = mapping.values()[0].header
        self.assertEqual(header, u'Portal Padrão Galeria de Vídeos')

        header_type = mapping.values()[0].header_type
        self.assertEqual(header_type, u'H4')

        show_active_title = mapping.values()[0].show_active_title
        self.assertEqual(show_active_title, True)

        show_inactive_title = mapping.values()[0].show_inactive_title
        self.assertEqual(show_inactive_title, True)

        show_description = mapping.values()[0].show_description
        self.assertEqual(show_description, True)

        show_footer = mapping.values()[0].show_footer
        self.assertEqual(show_footer, True)

        footer = mapping.values()[0].footer
        self.assertEqual(footer, u'Mais...')

        footer_url = mapping.values()[0].footer_url
        self.assertEqual(footer_url, self.videos['url'])

        limit = mapping.values()[0].limit
        self.assertEqual(limit, 2)

        collection = mapping.values()[0].collection
        self.assertEqual(collection, self.videos['path'])

    def test_renderer(self):
        r = self._assigned_renderer(self.videos)

        self.assertIsInstance(r, videogallery.Renderer)

    def test_renderer_cssclass(self):
        r1 = self._assigned_renderer(self.videos)

        self.assertEqual(r1.css_class(),
                         'brasil-gov-portlets-videogallery-portal-padrao-galeria-de-videos')

    def test_renderer_results(self):
        r = self._assigned_renderer(self.videos)

        results = [b.id for b in r.results()]
        self.assertEqual(results, ['video-2', 'video-3', 'video-1'])

    def test_renderer_collection(self):
        r = self._assigned_renderer(self.videos)

        self.assertEqual(r.collection(), self.videos['collection'])

    def test_renderer_header(self):
        r = self._assigned_renderer(self.videos)

        self.assertEqual(r.header(),
                         u'<h2 class="portlet-videogallery-header">Portal ' +
                         u'Padr&#227;o Galeria de V&#237;deos</h2>')

    def test_renderer_thumbnail(self):
        r1 = self._assigned_renderer(self.files)
        r2 = self._assigned_renderer(self.videos)

        videos = [r1.thumbnail(o) for o in r1.results()]
        self.assertEqual(videos, [None, None, None])

        videos = [r2.thumbnail(o) for o in r2.results()]
        video_order = [2, 3, 1]
        for i, video in enumerate(videos):
            self.assertIn('src', video)
            self.assertTrue(video['src'])
            self.assertIn('alt', video)
            self.assertEqual(video['alt'],
                             ('Video {0} description - Lorem ipsum dolor sit ' +
                              'amet, consectetur adipiscing elit. Donec ' +
                              'eleifend hendrerit interdum.')
                             .format(video_order[i]))
