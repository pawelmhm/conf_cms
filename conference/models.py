from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db import connection

class Abstract(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateTimeField('date_submitted')
    email = models.EmailField(max_length=100)
    content = models.TextField(max_length=1000)
    affiliation = models.CharField(max_length=200)

    def __init__(self,*args,**kwargs):
        super(Abstract,self).__init__(*args,**kwargs)
        self.avg = self.avgScore()

    def __unicode__(self):
        return "{author} - {title} - {date}".format(author=self.author,
                title=self.title[:20], date=self.date)

    def avgScore(self):
        # django has some problems with avg, resolving to raw sql
        query = "select avg(rating) from conference_comment as cc where cc.abstract_id = %s"
        cursor = connection.cursor()
        cursor.execute(query,[self.id])
        rows = cursor.fetchone()[0]
        return rows


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
    content = models.TextField(help_text="what do we think about this abstract",max_length=400)
    rating = models.IntegerField(help_text="value from 1 to 5",validators=[MinValueValidator(1),
        MaxValueValidator(5)])

    def __unicode__(self):
        return "{abstr} -- {author} -- {content} -- {rating}". \
            format(abstr=self.abstract.id,author=self.author,content=self.content,rating=self.rating)
