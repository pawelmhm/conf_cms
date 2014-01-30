from django.forms import ModelForm, HiddenInput
from conference.models import Abstract, Post, Participant
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

