from django.conf.urls import patterns, include, url
#from django.contrib import admin
import rest_framework
from conference import views
from conference.views import Abstracts,OneAbstract,PostsHtml,Logs,OnePost
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^admin/$',views.getAdmin, name="adminView"),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/abstracts/$', Abstracts.as_view(),name='abstractsView'),
    url(r'^admin/abstracts/(\d+)$', OneAbstract.as_view(),name='abstractsView'),
    url(r'^admin/posts/$',PostsHtml.as_view(),name="postView"),
    url(r'^admin/posts/(\d+)$',OnePost.as_view(),name="postView"),
    url(r'^admin/logs/$', Logs.as_view(),name="logs")
    )
