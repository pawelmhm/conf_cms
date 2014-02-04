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
from django.db import connection

from conference.models import Abstract,Post,Comment
from conference.forms import AbstractForm, PostForm, CommentForm
import datetime

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
            abstracts = Abstract.objects.all()
            posts = Post.objects.all()
            timedelta = datetime.date(2014,11,29) - datetime.date.today()
            timedelta = timedelta.days
            count = len(abstracts)
            abstracts = [a for a in list(abstracts) if a.avg == None]
            return render_to_response('admin.html',{"abstracts":abstracts,"posts":posts, "timedelta":timedelta,"count":count})
        else:
            form = AuthenticationForm()
            return render_to_response('login.html', {"form":form}, context_instance=RequestContext(request))

    def post(self,request,*args,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return render_to_response('admin.html')
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
        abstracts = sorted(list(abstracts),key=lambda a: a.avg,reverse=True)
        count = len(abstracts)
        return render_to_response('abstracts.html', {"abstracts":abstracts, "count":count})


class OneAbstract(ProtectedView):
    def simpleResponse(self,request,num,commentForm):
        abstract = Abstract.objects.filter(pk=num)
        if len(abstract) > 0:
            abstract = abstract[0]
        else:
            return redirect('/admin/')
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

class PostsHtml(ProtectedView):
    def get(self,request):
        posts = Post.objects.all()
        form = PostForm()
        return render_to_response('posts.html',{"posts":posts,"form":form})

class OnePost(ProtectedView):
    def baseResponse(self,request,num):
        pass

    def get(self,request,num):
        post = Post.objects.filter(pk=num)
        if len(post) == 0:
            return redirect('/admin/')
        postForm = PostForm(instance=post[0])
        return render_to_response('postDetail.html',{"form":postForm},context_instance=RequestContext(request))

    def post(self,request,num):
        postForm = PostForm(request.POST)
        if postForm.is_valid():
            post = Post.objects.filter(pk=num).update(title=request.POST["title"],content=request.POST["content"])
            return redirect('/admin/posts/')
        else:
            return redirect('/admin/posts/%s' % (num,))

    def delete(self,request,num):
        posts = Post.objects.filter(pk=num)
        posts.delete()
        return HttpResponse("Items deleted")

class AddPost(ProtectedView):
    def get(self,request):
        form = PostForm()
        return render_to_response('postDetail.html',{"form":form},context_instance=RequestContext(request))

    def post(self,request):
        postForm = PostForm(request.POST)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.date = datetime.datetime.utcnow().replace(tzinfo=utc)
            post.save()
            return redirect('/admin/posts/')
        else:
            return render_to_response('postDetail.html',{"form":postForm},context_instance=RequestContext(request))
