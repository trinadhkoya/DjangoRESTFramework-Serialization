from django.conf.urls import url
from snippets import views


urlpatterns = [
    url(r'^snippets/$', views.snippet_list),

    url(r'^snippets/(?P<key>[0-9]+)/$', views.snippet_detail),
]