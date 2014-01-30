# Create your views here.

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.utils.timezone import utc

from conference.models import Abstract,Post
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conference.serializers import AbstractSerial
from conference.forms import AbstractForm, PostForm
import datetime

class JSONResponse(HttpResponse):
    def __init__(self, data, *args,**kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = 'application/json'
        super(JSONResponse, self).__init__(content,**kwargs)

class Abstracts(View):
    def get(self,request,*args,**kwargs):
        abstracts = Abstract.objects.all()
        return render_to_response('abstracts.html', {"abstracts":abstracts})

    def post(self,request):
        form = AbstractForm(request.POST)
        if form.is_valid():
            abstr = form.save(commit=False)
            abstr.date = datetime.datetime.utcnow().replace(tzinfo=utc)
            abstr.save()
            return JSONResponse('all clear')
        else:
            return redirect('/#register')#JSONResponse(form.errors)

class OneAbstract(View):
    def get(self,request,num):
        abstract = Abstract.objects.get(pk=num)
        return render_to_response('oneAbstract.html',{"abstract":abstract,
            "num":num})

class PostView(View):
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

class OnePost(View):
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

class Logs(View):
    def get(self,request):
        return render_to_response('logs.html')

def home(request,**kwargs):
    content = {}
    keyArticles = ["keynotes","about","clp","gettingThere","technical"]
    for keyword in keyArticles:
        article = Post.objects.filter(keyword=keyword)
        if len(article) >= 1:
            content[keyword] = article[0]

    if request.method == "POST":
        form = AbstractForm(request.POST)
        if form.is_valid():
            abstr = form.save(commit=False)
            abstr.date = datetime.datetime.utcnow().replace(tzinfo=utc)
            abstr.save()
            return redirect('/') #HttpResponse(status=201)
        else:
            content["form"] = form
            return render_to_response('index.html',content,
            context_instance=RequestContext(request))

    elif request.method == "GET":
        content["form"] = AbstractForm()
        return render_to_response('index.html',content,
            context_instance=RequestContext(request))

def getAdmin(request):
    return render_to_response('admin.html')

def getArticles():
    pass
