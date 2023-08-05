from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'feincms_banners.views',
    url(r'^b/c/(?P<code>[^/]+)/$', 'click', name='banner_click'),
    url(r'^b/i/(?P<code>[^/]+)/$', 'impression', name='banner_impression'),
)
