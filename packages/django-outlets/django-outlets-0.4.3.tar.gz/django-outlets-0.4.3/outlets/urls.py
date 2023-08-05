"""URLs for the outlet app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[\w|-]+)/$', views.OutletsListView.as_view(),
        name='outlets_list'),
    url(r'^infobox/(?P<pk>\d+)/$', views.MapMarkerInfoboxAJAXView.as_view(),
        name='outlets_mapmarker_info'),
    url(r'^$', views.OutletsListView.as_view(), name='outlets_list'),
)
