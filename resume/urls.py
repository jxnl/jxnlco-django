from django.conf.urls import patterns, url
from resume import views

urlpatterns = patterns('',
                       url(r'^resume/$', views.resume, name='resume'),
                      )

