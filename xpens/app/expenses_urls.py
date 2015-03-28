from django.conf.urls import patterns, url

from .expenses_views import (
    NewExpenseView,
    ListExpensesView,
    UpdateExpenseView,
    DeleteExpenseView,
    SearchExpenseView
)

urlpatterns = patterns('',
                       url(r'^$', ListExpensesView.as_view(),
                           name="list_expenses"),
                       url(r'^(?P<from_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/to/(?P<to_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/$', ListExpensesView.as_view(),
                           name="list_expenses_date_range"),
                       url(r'^search/$', SearchExpenseView.as_view(),
                           name="search_expenses"),
                       url(r'^category/(?P<category_id>\d+)/$',
                           ListExpensesView.as_view(),
                           name="list_expenses_category"),
                       url(r'^category/(?P<category_id>\d+)/(?P<from_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/to/(?P<to_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/$',
                           ListExpensesView.as_view(),
                           name="list_expenses_category_date_range"),
                       url(r'^new/$', NewExpenseView.as_view(),
                           name="new_expense"),
                       url(r'^(?P<pk>\d+)/update/$',
                           UpdateExpenseView.as_view(),
                           name="update_expense"),
                       url(r'^(?P<pk>\d+)/delete/$',
                           DeleteExpenseView.as_view(),
                           name="delete_expense"),
                       )
