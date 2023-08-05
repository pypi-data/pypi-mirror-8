"""
Urls for porticus
"""
from django.conf.urls.defaults import url, patterns
from porticus.views import GalleryListView, GalleryDetailView, GalleryTreeView, AlbumDetailView, TagsView, TagDetailView

urlpatterns = patterns('porticus.views',
    url(r'^$', GalleryListView.as_view(), name='porticus-galleries-index'),
    
    url(r'^tags/$', TagsView.as_view(), name='tags-index'),
    url(r'^tag/(?P<tags>[-_A-Za-z0-9]+)/$', TagDetailView.as_view()),
    
    url(r'^(?P<detail_slug>[-\w]+)/$', GalleryDetailView.as_view(), name='porticus-gallery-detail'),
    url(r'^tree/(?P<detail_slug>[-\w]+)/$', GalleryTreeView.as_view(), name='porticus-gallery-tree'),
    
    url(r'^(?P<parent_slug>[-\w]+)/(?P<detail_slug>[-\w]+)/$', AlbumDetailView.as_view(), name='porticus-album-detail'),
)
