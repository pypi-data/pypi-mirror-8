# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from django.test import TestCase
from facebook_api.utils import get_or_create_from_small_resource
from facebook_posts.models import Post

from .factories import PageFactory
from .models import Page, PAGES_FANS_USER_ID
from .parser import FacebookPageFansParser

PAGE_ID = '19292868552'
PAGE_RESOURCE_SHORT = {'category': 'Product/service', 'id': PAGE_ID, 'name': 'Facebook Developers'}
PAGE_URL = 'https://www.facebook.com/pages/METRO-Cash-and-Carry-Russia/129107667156177'
PAGE_FANS_ID = 501842786534856


class FacebookPagesTest(TestCase):

    def test_fetch_page(self):

        self.assertEqual(Page.objects.count(), 0)
        page = Page.remote.fetch(PAGE_ID)
        page = Page.remote.fetch(PAGE_ID)
        self.assertEqual(Page.objects.count(), 1)

        self.assertEqual(page.graph_id, PAGE_ID)
        self.assertEqual(page.name, 'Facebook Developers')
        self.assertEqual(page.is_published, True)
        self.assertEqual(page.website, 'http://developers.facebook.com')
        self.assertEqual(page.category, "Product/service")
        self.assertEqual(page.username, 'FacebookDevelopers')
        self.assertEqual(page.link, 'https://www.facebook.com/FacebookDevelopers')
        self.assertGreater(len(page.company_overview), 0)
        self.assertGreater(page.likes_count, 0)

        page.username = page.website = ''
        self.assertEqual(page.username, '')
        self.assertEqual(page.website, '')
        page.save()
        page = Page.remote.fetch(PAGE_ID)
        self.assertEqual(page.username, 'FacebookDevelopers')
        self.assertEqual(page.website, 'http://developers.facebook.com')

    def test_get_by_url(self):

        page = Page.remote.get_by_url('https://www.facebook.com/pages/METRO-Cash-and-Carry-Russia/129107667156177')

        self.assertEqual(page.graph_id, '129107667156177')
        self.assertEqual(page.name, 'METRO Cash and Carry Russia')
        self.assertEqual(page.is_published, True)
        self.assertEqual(page.website, 'http://www.metro-cc.ru')

    def test_fetch_page_from_resource(self):

        Page.remote.fetch(PAGE_ID)

        page = get_or_create_from_small_resource(PAGE_RESOURCE_SHORT)
        self.assertEqual(page.name, PAGE_RESOURCE_SHORT['name'])
        self.assertEqual(page.category, PAGE_RESOURCE_SHORT['category'])

        page1 = Page.objects.all()[0]
        self.assertEqual(page1.website, "http://developers.facebook.com")

        page2 = get_or_create_from_small_resource(PAGE_RESOURCE_SHORT)
        self.assertEqual(page2.website, "http://developers.facebook.com")
        self.assertEqual(page2.category, PAGE_RESOURCE_SHORT['category'])


class FacebookPageFansTest(TestCase):

    def test_get_parser_response(self):

        parser = FacebookPageFansParser(
            authorized=True, url='/ajax/browser/list/page_fans/?page_id=%s&start=0&__user=%s&__a=1' % (PAGE_FANS_ID, PAGES_FANS_USER_ID))
        self.assertIsInstance(parser.content_bs, BeautifulSoup)

    def test_fetch_fans_ids(self):

        page = PageFactory(graph_id=PAGE_FANS_ID)

        ids = page.fetch_fans_ids_parser()
        self.assertGreater(len(ids), 450)
