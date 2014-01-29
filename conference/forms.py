from django.forms import ModelForm
from conference.models import Abstract, Post, Participant

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
