import unittest

from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Ad

class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # print("setUpTestData: Run once to set up non-modified data for all class methods.")
        Ad.objects.create(title='Big', description='Bob', category='Bobobob')
        pass

    def test_Ad_title(self):
        author = Ad.objects.get(id=1)
        title = author._meta.get_field('title').verbose_name
        self.assertEquals(title, 'title')

    def test_Ad_description(self):
        author = Ad.objects.get(id=1)
        description = author._meta.get_field('description').verbose_name
        self.assertEquals(description, 'description')

    def test_Ad_title_image(self):
        author = Ad.objects.get(id=1)
        title_image = author._meta.get_field('title_image').verbose_name
        self.assertEquals(title_image, 'title image')

    def test_Ad_title_video(self):
        author = Ad.objects.get(id=1)
        title_video = author._meta.get_field('title_video').verbose_name
        self.assertEquals(title_video, 'title video')

    def test_Ad_title_audio(self):
        author = Ad.objects.get(id=1)
        title_audio = author._meta.get_field('title_audio').verbose_name
        self.assertEquals(title_audio, 'title audio')

    def test_Ad_category(self):
        author = Ad.objects.get(id=1)
        category = author._meta.get_field('category').verbose_name
        self.assertEquals(category, 'category')

    def test_description_max_length(self):
        author=Ad.objects.get(id=1)
        max_length = author._meta.get_field('description').max_length
        self.assertEquals(max_length,500)

    def test_object_name_is_title_comma_description(self):
        author = Ad.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.title, author.description)
        self.assertEquals(expected_object_name, str(author))

class AdListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 13 authors for pagination tests
        number_of_authors = 6
        for author_num in range(number_of_authors):
            Ad.objects.create(title='Christian %s' % author_num, description='Surname %s' % author_num,)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exists_at_desired_location2(self):
        resp = self.client.get('/accounts/profile/')
        self.assertEqual(resp.status_code, 200)

        # ads_ads /
    def test_view_url_exists_at_desired_location3(self):
        resp = self.client.get('/signup/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exists_at_desired_location4(self):
        resp = self.client.get('/accounts/logout/')
        self.assertEqual(resp.status_code, 302)



