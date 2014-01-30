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
import json

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.fake = Factory.create()
        keywords = ["keynotes","about","clp","gettingThere","technical"]
        for key in keywords:
            post = Post(title=self.fake.sentence(),
                content="\n".join(self.fake.paragraphs(nb=7)),
                date=datetime.datetime.utcnow().replace(tzinfo=utc),
                keyword=key)
            if key == "about":
                self.testPost = post
            post.save()

        self.adminPages = ['posts','abstracts','logs']

        abstract = Abstract(title=self.fake.sentence(),
                author=self.fake.name(),content=self.fake.text(),
                email=self.fake.email(),
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

    def testPostAbstract(self):
        fakeAbs = {"author": self.fake.name(),
                "content":"\n".join(self.fake.paragraphs(nb=5)),
            "affiliation":self.fake.word(),
            "title":self.fake.sentence(),
            "email":self.fake.email(),
            "date":datetime.datetime.utcnow().replace(tzinfo=utc)}

        # ensure there is no abstract with this title before post
        checkDb = Abstract.objects.filter(title=fakeAbs["title"])
        self.assertEqual(len(checkDb),0)

        # now actually post fake abstract
        response = self.client.post("/admin/abstracts/", fakeAbs, follow=True)
        self.assertEqual(response.status_code,200)
        responseJson = json.loads(response.content)
        self.assertEqual(responseJson,"all clear")

        # even if response is valid it can not be in database
        checkDb = Abstract.objects.filter(title=fakeAbs["title"])
        self.assertNotEqual(len(checkDb),0)
        self.assertEqual(checkDb[0].title,fakeAbs["title"])

    def testPostInvalidAbs(self):
        # invalid all fields blank
        fakeAbs = {"author": "", "content":"",
            "affiliation":"", "title":"","email":""}
        response = self.client.post('/admin/abstracts/',fakeAbs,follow=True)
        responseJson = json.loads(response.content)
        self.assertEqual(response.status_code,200)
        # it should stil return 200
        # but with errors
        self.assertNotIn('all clear',response.content)

    def testPostInvalidAbsTwo(self):
        # too long fields
        fakeAbs = {"author":"<script>alert('sss')</script>",
                "title":"".join(self.fake.paragraphs(nb=100)),
                "content":self.fake.sentence(),"email":self.fake.email(),
                "affiliation":self.fake.name()}
        response = self.client.post('/admin/abstracts/',fakeAbs,follow=True)
        responseJson = json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertNotIn("all clear",responseJson)

    def testPostSpam(self):
        # test spam blocker
        pass

