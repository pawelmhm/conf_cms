from rest_framework import serializers
from conference.models import Abstract,Post

class AbstractSerial(serializers.ModelSerializer):
    class Meta:
        model = Abstract
        fields = ('id', 'title', 'author','date', 'email', 'content', 'affiliation')
