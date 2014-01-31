from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

class Abstract(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateTimeField('date_submitted')
    email = models.EmailField(max_length=100)
    content = models.TextField(max_length=1000)
    affiliation = models.CharField(max_length=200)

    def __unicode__(self):
        return "{author} - {title} - {date}".format(author=self.author,
                title=self.title[:20], date=self.date)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField('date_submitted')
    keyword = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    affiliation = models.CharField(max_length=100)

class Comment(models.Model):
    abstract = models.ForeignKey('Abstract')
    author = models.ForeignKey(User)
    content = models.TextField(max_length=400)
    rating = models.IntegerField(validators=[MinValueValidator(1),
        MaxValueValidator(5)])

    def __unicode__(self):
        return "{abstr} -- {author} -- {content} -- {rating}". \
            format(abstr=self.abstract.id,author=self.author,content=self.content,rating=self.rating)
