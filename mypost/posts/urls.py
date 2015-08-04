from django.conf.urls import url
from mypost import views as main_view

from . import views
urlpatterns = [
    url(r'^$', main_view.index, name='index'),
    url(r'^(?P<title_id>[0-9]+)/$', views.view_post, name='view_post'),
    url(r'^(?P<title_id>[0-9]+)/category/$',
        views.view_category, name='view_category'),
    url(r'^(?P<title_id>[0-9]+)/edit/$', views.view_edit, name='view_edit'),
]
