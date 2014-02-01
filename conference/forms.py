from django.forms import ModelForm, HiddenInput
from conference.models import Abstract, Post, Participant, Comment
from django.contrib.auth.models import Permission, User

class AbstractForm(ModelForm):
    class Meta:
        model = Abstract
        fields = ["title","author","email","content","affiliation"]

class NoAbstract(ModelForm):
    class Meta:
        model = Participant

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","content"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content","rating"]
