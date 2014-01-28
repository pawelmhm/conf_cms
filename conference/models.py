from django.db import models

# Create your models here.

class Abstract(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateTimeField('date_submitted')
    email = models.EmailField(max_length=100)
    content = models.TextField()
    affiliation = models.CharField(max_length=200)

    def __unicode__(self):
        return "{author} - {title} - {date}".format(author=self.author,
                title=self.title[:20], date=self.date)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField('date_submitted')

    def __unicode__(self):
        return self.title
