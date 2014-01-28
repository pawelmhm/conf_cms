# Create your views here.

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.shortcuts import render_to_response
from conference.models import Abstract,Post
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from conference.serializers import AbstractSerial

class JSONResponse(HttpResponse):
    def __init__(self, data, *args,**kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = 'application/json'
        super(JSONResponse, self).__init__(content,**kwargs)

def home(request):
    # will return bootrstrapped raw html
    # in which there will be some Mustache
    # elements, the rest is going to be
    # fetched from our rest server
    return HttpResponse(render_to_string('index.html'))

def getAdmin(request):
    return render_to_response('admin.html')

class Abstracts(View):
    def get(self,request,*args,**kwargs):
        abstracts = Abstract.objects.all()
        #serialAbs = AbstractSerial(abstracts,many=True)
        #return JSONResponse(serialAbs.data)
        return render_to_response('abstracts.html', {"abstracts":abstracts})

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
        return render_to_response('posts.html', posts)

class OnePost(PostView):
    def get(self,request,num):
        return render_to_response('postDetail.html', self.getOne(num))

class Logs(View):
    def get(self,request):
        return render_to_response('logs.html')
