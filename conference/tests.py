"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from faker import Factory
from conference.models import Post, Abstract
import datetime
from django.utils.timezone import utc

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        fake = Factory.create()
        keywords = ["keynotes","about","clp","gettingThere","technical"]
        for key in keywords:
            post = Post(title=fake.sentence(),
                content="\n".join(fake.paragraphs(nb=7)),
                date=datetime.datetime.utcnow().replace(tzinfo=utc),
                keyword=key)
            if key == "about":
                self.testPost = post
            post.save()

        self.adminPages = ['posts','abstracts','logs']

        abstract = Abstract(title=fake.sentence(),
                author=fake.name(),content=fake.text(),
                email=fake.email(),
                date=datetime.datetime.utcnow().replace(tzinfo=utc)
                )
        self.testAbs = abstract
        abstract.save()

    def testHomePage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

    def testAdmin(self):
        response = self.client.get('/admin/')
        self.assertEqual(200,response.status_code)

    def testAllGets(self):
        for page in self.adminPages:
            response = self.client.get('/admin/'+page+'/')
            self.assertEqual(response.status_code,200)

    def testAbstracts(self):
        abstracts = Abstract.objects.all()
        self.assertNotEqual(len(abstracts),0)
        firstAbs = Abstract.objects.get(pk=1)
        self.assertEqual(firstAbs.id,1)

    def testAllSubPages(self):
        uts = [self.testPost,self.testAbs]
        i = 0
        for page in self.adminPages[:2]:
            url = '/admin/{page}/{id}'.format(page=page,id=uts[i].id)
            response = self.client.get(url)
            self.assertEqual(response.status_code,200,
                    "{status}  {url}".format(
                        status=response.status_code,url=url))
            i += 1

    def testAuthentication(self):
        pass

    def testDelete(self):
        posts = Post.objects.all()
        before = len(posts)
        self.client.delete('/admin/posts/%s' % (posts[0].id,))
        after = len(Post.objects.all())
        self.assertEqual(before-1,after)
