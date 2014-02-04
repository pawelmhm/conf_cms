"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from faker import Factory
from conference.models import Post, Abstract, Comment, User
import datetime
from django.utils.timezone import utc
import json

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.fake = Factory.create()
        self.keywords = ["keynotes","about","clp","gettingThere","technical"]
        self.adminPages = ['posts','abstracts']

        # generate some fake data
        self.fakePosts()
        self.fakeAbstracts(5)
        self.fakeUsers(5)
        self.insertComment(4)

    def fakePosts(self):
        for key in self.keywords:
            post = Post(title=self.fake.sentence(),
                content="\n".join(self.fake.paragraphs(nb=7)),
                date=datetime.datetime.utcnow().replace(tzinfo=utc),
                keyword=key)
            if key == "about":
                self.testPost = post
            post.save()

    def fakeAbstracts(self,howMany):
        for i in range(howMany):
            abstract = Abstract(title=self.fake.sentence(),
                author=self.fake.name(),content=self.fake.text(),
                email=self.fake.email(),
                date=datetime.datetime.utcnow().replace(tzinfo=utc))
            abstract.save()

        self.testAbs = abstract

    def fakeUsers(self,howMany):
        for i in range(howMany):
            fakePass = self.fake.last_name()
            user = User.objects.create_user(self.fake.first_name(),self.fake.email(),fakePass)
            user.save()
        self.user = user
        self.fakePass = fakePass

    def insertComment(self,num):
        for i in range(num):
            com = Comment(abstract=self.testAbs,author=self.user,
                content=self.fake.sentence(),rating=4)
            com.save()

    def getAdminPages(self,status_code):
        for page in self.adminPages:
            response = self.client.get('/admin/'+page+'/')
            self.assertEqual(response.status_code,status_code)


    def getAdminSubPages(self,status_code):
        uts = [self.testPost,self.testAbs]
        i = 0
        for page in self.adminPages[:2]:
            url = '/admin/{page}/{id}'.format(page=page,id=uts[i].id)
            response = self.client.get(url)
            self.assertEqual(response.status_code,status_code,
                    "{status}  {url}".format(status=response.status_code,url=url))
            i += 1

class DbTest(SimpleTest):
    def testSaveComment(self):
        before = len(Comment.objects.all())
        self.insertComment(1)
        after = len(Comment.objects.all())
        self.assertEqual(before+1,after)

    def testGetComment(self):
        self.insertComment(1)
        com = Comment.objects.filter(abstract__exact=self.testAbs)
        self.assertEqual(len(com),1)

class TestOpen(SimpleTest):
    # tests all views that are available to the public
    # (not protected, no need for login)
    def testHomePage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

    def testAdmin(self):
        response = self.client.get('/admin/')
        self.assertEqual(200,response.status_code)

    def testAllGets(self):
        # should return 302, user not logged in
        self.getAdminPages(302)

    def testAbstracts(self):
        abstracts = Abstract.objects.all()
        self.assertNotEqual(len(abstracts),0)

    def testAllSubPages(self):
        # no login all subpages should return 302
        self.getAdminSubPages(302)

    def testDelete(self):
        # User not logged. Delete should have no effect
        posts = Post.objects.all()
        before = len(posts)
        self.client.delete('/admin/posts/%s' % (posts[0].id,))
        after = len(Post.objects.all())
        self.assertEqual(before,after)

    def testPostAbstract(self):
        # abstracts should go through
        # no need to login to post abstracts

        fakeAbs = {"author": self.fake.name(),
                "content":"\n".join(self.fake.paragraphs(nb=5)),
            "affiliation":self.fake.word(),
            "title":self.fake.sentence(),
            "email":self.fake.email(),
            "date":datetime.datetime.utcnow().replace(tzinfo=utc)}

        # ensure there is no abstract with this title before post
        checkDb = Abstract.objects.filter(title=fakeAbs["title"])
        self.assertEqual(len(checkDb),0)

        # now actually post it
        response = self.client.post("/", fakeAbs, follow=True)
        self.assertEqual(response.status_code,200)

        # response 200, great, but is it in database?
        checkDb = Abstract.objects.filter(title=fakeAbs["title"])
        self.assertNotEqual(len(checkDb),0)
        self.assertEqual(checkDb[0].title,fakeAbs["title"])
        self.assertIn('Thank you for submission.',response.content)

    def testPostInvalidAbs(self):
        # invalid all fields blank

        fakeAbs = {"author": "", "content":"",
            "affiliation":"", "title":"","email":""}
        checkDb = Abstract.objects.filter(title=fakeAbs["title"])
        self.assertEqual(len(checkDb),0)

        response = self.client.post('/',fakeAbs,follow=True)
        self.assertEqual(response.status_code,200)

        checkDb = Abstract.objects.filter(title=fakeAbs["title"])
        self.assertEqual(len(checkDb),0)

        self.assertIn('field is required',response.content)

    def testPostInvalidAbsTwo(self):
        # too long fields
        fakeAbs = {"author":self.fake.name(),
                "title":"".join(self.fake.paragraphs(nb=100)),
                "content":self.fake.sentence(),"email":self.fake.email(),
                "affiliation":self.fake.name()}
        response = self.client.post('/',fakeAbs,follow=True)
        self.assertEqual(response.status_code,200)

class TestAuth(SimpleTest):
    def login(self):
        self.client.login(username=self.user.username,password=self.fakePass)

    def testAllAdminPagesGet(self):
        # all admin pages should be visible
        # no redirection should take place
        self.login()
        self.getAdminPages(200)

    def testAdminSubPages(self):
        # same story for subpages
        # all should be available
        self.login()
        self.getAdminSubPages(200)

    def testAbstractGet(self):
        self.login()
        response = self.client.get('/admin/abstracts/')
        self.assertEqual(response.status_code,200)

    def testPostComment(self):
        self.login()
        abstr = Abstract.objects.all()[0]
        before = len(Comment.objects.all())
        comment = {"content":self.fake.sentence(),"rating":4}
        response = self.client.post('/admin/abstracts/%s' % (abstr.id,), comment)
        self.assertEqual(response.status_code,302)
        after = len(Comment.objects.all())
        self.assertEqual(before+1,after)

    def testPostInvalidComment(self):
        self.login()
        abstr = Abstract.objects.all()[0]
        response = self.client.post('/admin/abstracts/%s' % (abstr.id,), {"rating":29,"content":""},follow=True)
        self.assertIn('required',response.content)

        response = self.client.post('/admin/abstracts/%s' % (abstr.id), {"rating":29,"content":self.fake.sentence()},follow=True)
        self.assertIn("less than or equal to 5",response.content)

    def testAddPost(self):
        self.login()
        response = self.client.get('/admin/posts/new')
        self.assertEqual(response.status_code,200)

        data = {"title":self.fake.word(),"keyword":"about","content":self.fake.sentence()}
        response = self.client.post('/admin/posts/new',data,follow=True)
        self.assertEqual(response.status_code,302)

    def testInvalidAddPost(self):
        self.login()
        data = {"title":"","keyword":"","content":""}
        response = self.client.post('/admin/posts/new',data)
        self.assertEqual(response.status_code,200)
        self.assertIn('the field is required',response.content)
