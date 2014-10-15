from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    
    url(r'^', include('swFondoIP.apps.tramiteDoc.urls')),
    url(r'^', include('swFondoIP.apps.home.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
