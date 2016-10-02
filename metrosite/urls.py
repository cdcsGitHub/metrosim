from django.conf.urls import patterns, include, url
from metro.views import index, runtrains, charts
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^first/$',index),
    url(r'^loading/$', runtrains),
    url(r'^charts/$', charts),

    # Examples:
    # url(r'^$', 'metrosite.views.home', name='home'),
    # url(r'^metrosite/', include('metrosite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
