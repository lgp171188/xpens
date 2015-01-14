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
                       url(r'^expenses/$',
                           ListExpensesView.as_view(),
                           name="list_expenses"),
                       url(r'^expenses/search/$',
                           SearchExpenseView.as_view(),
                           name="search_expenses"),
                       url(r'^expenses/category/(?P<category_id>\d+)/$',
                           ListCategoryExpensesView.as_view(),
                           name="list_expenses_category"),
                       url(r'^expenses/new/$',
                           NewExpenseView.as_view(),
                           name="new_expense"),
                       url(r'^categories/$',
                           ListCategoriesView.as_view(),
                           name="list_categories"),
                       url(r'^categories/new/$',
                           NewCategoryView.as_view(),
                           name="new_category"),
                       url(r'^expense/(?P<pk>\d+)/update/$',
                           UpdateExpenseView.as_view(),
                           name="update_expense"),
                       url(r'^category/(?P<pk>\d+)/update/$',
                           UpdateCategoryView.as_view(),
                           name="update_category"),
                       url(r'^expense/(?P<pk>\d+)/delete/$',
                           DeleteExpenseView.as_view(),
                           name="delete_expense"),
                       url(r'^category/(?P<pk>\d+)/delete/$',
                           DeleteCategoryView.as_view(),
                           name="delete_category"),
                       url(r'^statistics/categories/(?P<from_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/to/(?P<to_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/$',
                           StatisticsView.as_view(),
                           name="statistics_custom"),
                       url(r'^statistics/categories/$',
                           StatisticsView.as_view(),
                           name="statistics"),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r'^api/', include('app.api_urls')),
)

if settings.REGISTRATION_ENABLED:
    urlpatterns += patterns('',
                            url(r'^register/$',
                                RegistrationView.as_view(),
                                name="register"),
                   )
