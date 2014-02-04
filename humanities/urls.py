from django.conf.urls import patterns, include, url
from conference import views
from conference.views import Abstracts,OneAbstract,PostsHtml,OnePost,Home,Admin,AddPost

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/$',Admin.as_view(), name="adminView"),
    url(r'^admin/abstracts/$', Abstracts.as_view(),name='abstractsView'),
    url(r'^admin/abstracts/(\d+)$', OneAbstract.as_view(),name='abstractsView'),
    url(r'^admin/posts/$',PostsHtml.as_view(),name="postView"),
    url(r'^admin/posts/(\d+)$',OnePost.as_view(),name="onePostView"),
    url(r'^admin/posts/new$',AddPost.as_view(),name="addPost"),
    url(r'^admin/logout/$',views.viewLogout)
    )
