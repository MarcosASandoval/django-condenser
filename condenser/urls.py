from django.conf.urls import patterns, url

from condenser import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^condense$', views.condense, name='condense'),
    url(r'^inspector$', views.inspector, name='inspector'),
)
