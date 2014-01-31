from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from conference.models import Abstract,Post,Comment
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conference.serializers import AbstractSerial
from conference.forms import AbstractForm, PostForm, CommentForm
import datetime

class JSONResponse(HttpResponse):
    def __init__(self, data, *args,**kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = 'application/json'
        super(JSONResponse, self).__init__(content,**kwargs)

class Home(View):
    def get_articles(self):
        content = {}
        keyArticles = ["keynotes","about","clp","gettingThere","technical"]
        for keyword in keyArticles:
            article = Post.objects.filter(keyword=keyword)
            if len(article) >= 1:
                content[keyword] = article[0]
        return content

    def get(self,request,**kwargs):
        content = self.get_articles()
        content["form"] = AbstractForm()
        return render_to_response('index.html',content,
            context_instance=RequestContext(request))

    def post(self,request):
        content = self.get_articles()
        form = AbstractForm(request.POST)
        if form.is_valid():
            abstr = form.save(commit=False)
            abstr.date = datetime.datetime.utcnow().replace(tzinfo=utc)
            abstr.save()
            return redirect('/')
        else:
            content["form"] = form
            return render_to_response('index.html',content,
            context_instance=RequestContext(request))

#
# Admin backend
#


class Admin(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return render_to_response('admin.html')
        else:
            form = AuthenticationForm()
            return render_to_response('login.html', {"form":form}, context_instance=RequestContext(request))

    def post(self,request,*args,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return render_to_response('admin.html')
            else:
                pass
        else:
            form = AuthenticationForm(request.POST)
            return render_to_response('login.html',{"form":form},context_instance=RequestContext(request))

def viewLogout(request):
    logout(request)
    return redirect('/')

class ProtectedView(View):
    @method_decorator(login_required)
    def dispatch(self,*args,**kwargs):
        return super(ProtectedView,self).dispatch(*args,**kwargs)

class Abstracts(ProtectedView):
    def get(self,request,*args,**kwargs):
        abstracts = Abstract.objects.all()
        return render_to_response('abstracts.html', {"abstracts":abstracts})

class OneAbstract(ProtectedView):
    def simpleResponse(self,request,num,commentForm):
        abstract = Abstract.objects.get(pk=num)
        comments = Comment.objects.filter(abstract__exact=abstract)
        return render_to_response('oneAbstract.html',{"abstract":abstract,
            "num":num, "commentForm":commentForm, "comments": comments},context_instance=RequestContext(request))

    def get(self,request,num,*args,**kwargs):
        commentForm = CommentForm()
        return self.simpleResponse(request,num,commentForm)

    def post(self,request,num):
        # post here posts a comment on a given abstract
        # abstracts themselves should not be modified at all
        abstr = Abstract.objects.get(pk=num)
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = Comment(abstract=abstr,author=request.user,
                    content=request.POST["content"],rating=request.POST["rating"])
            comment.save()
            return redirect('/admin/abstracts/%s' % (num,))
        else:
            return self.simpleResponse(request,num,commentForm)


class PostView(ProtectedView):
    def getAll(self):
        posts = Post.objects.all()
        return {"posts":posts}

    def getOne(self,num):
        post = Post.objects.get(pk=num)
        return {"post":post}

class PostsHtml(PostView):
    def get(self,request):
        posts = self.getAll()
        form = PostForm()
        posts["form"] = form
        return render_to_response('posts.html',posts)

class OnePost(PostView):
    def get(self,request,num):
        c = {}
        c.update(csrf(request))
        post = Post.objects.get(pk=num)
        postForm = PostForm(instance=post)
        return render_to_response('postDetail.html',{"form":postForm},context_instance=RequestContext(request))

    def post(self,request,num):
        postForm = PostForm(request.POST)
        post = Post.objects.filter(pk=num).update(title=request.POST["title"],content=request.POST["content"])
        return redirect('/admin/posts')

    def delete(self,request,num):
        posts = Post.objects.filter(pk=num)
        posts.delete()
        return HttpResponse("Items deleted")

class Logs(ProtectedView):
    def get(self,request):
        return render_to_response('logs.html')

