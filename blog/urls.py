from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^archive/$', views.archive, name='archive'),
                       url(r'^blog/$', views.blog, name='blog'),
                       url(r'^projects/$', views.projects, name='projects'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^(?P<style>\w+)/(?P<key>\d+)/',
                           views.post, name='post'),
                       )
