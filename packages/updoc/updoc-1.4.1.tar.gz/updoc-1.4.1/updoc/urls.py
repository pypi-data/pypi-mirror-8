# -*- coding: utf-8 -*-
"""Define mappings from the URL requested by a user to a proper Python view."""
from django.conf.urls import patterns, url

__author__ = "flanker"

urlpatterns = patterns(  # pylint: disable=C0103
    '',
    url(r'^delete_doc/(?P<doc_id>\d+)/$', 'updoc.views.delete_doc'),
    url(r'^delete_url/(?P<url_id>\d+)/$', 'updoc.views.delete_url'),
    url(r'^show/(?P<doc_id>\d+)/(?P<path>.*)$', 'updoc.views.show_doc'),
    url(r'^show_alt/proxy.pac$', 'updoc.views.show_proxies'),
    url(r'^show_alt/(?P<doc_id>\d+)/(?P<path>.*)$', 'updoc.views.show_doc_alt'),
    url(r'^edit/(?P<doc_id>\d+)/$', 'updoc.views.edit_doc'),
    url(r'^my_docs/$', 'updoc.views.my_docs'),
    url(r'^download/(?P<doc_id>\d+)/(?P<fmt>zip|bz2|gz|xz)/$', 'updoc.views.compress_archive'),
    url(r'^favorite/(?P<root_id>\d+)/$', 'updoc.views.show_favorite'),
    url(r'^favorite/', 'updoc.views.show_favorite'),
    url(r'^upload_api/', 'updoc.views.upload_api'),
)