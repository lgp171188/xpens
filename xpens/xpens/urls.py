from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from app.views import *
from user_mgmt.views import *

urlpatterns = patterns('',
                       url(r'^$', HomeView.as_view(), name="home"),
                       url(r'^login/$', LoginView.as_view(),
                           {
                               "template_name" : "app/login.html",
                               "extra_context" : { "next" : reverse_lazy('home') },
                           },
                           name="login"),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {
                               "next_page" : reverse_lazy('login'),
                           },
                           name="logout"),
                       url(r'^password/change/$',
                           PasswordChangeView.as_view(),
                           name="password_change"),
                       url(r'^overview/$', OverviewView.as_view(),
                           name="overview"),

                       url(r'^expenses/', include('app.expenses_urls')),
                       url(r'^categories/', include('app.categories_urls')),
                       url(r'^statistics/', include('app.statistics_urls')),
                       url(r'^captcha/', include('captcha.urls')),
)

if settings.REGISTRATION_ENABLED:
    urlpatterns += patterns('',
                            url(r'^register/$',
                                RegistrationView.as_view(),
                                name="register"),
                   )
