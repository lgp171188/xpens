from django.conf.urls import patterns, url

from .expenses_views import (
    NewExpenseView,
    ListExpensesView,
    ListCategoryExpensesView,
    UpdateExpenseView,
    DeleteExpenseView,
    SearchExpenseView
)

urlpatterns = patterns('',
                       url(r'^$', ListExpensesView.as_view(),
                           name="list_expenses"),
                       url(r'^search/$', SearchExpenseView.as_view(),
                           name="search_expenses"),
                       url(r'^category/(?P<category_id>\d+)/$',
                           ListCategoryExpensesView.as_view(),
                           name="list_expenses_category"),
                       url(r'^new/$', NewExpenseView.as_view(),
                           name="new_expense"),
                       url(r'^(?P<pk>\d+)/update/$',
                           UpdateExpenseView.as_view(),
                           name="update_expense"),
                       url(r'^(?P<pk>\d+)/delete/$',
                           DeleteExpenseView.as_view(),
                           name="delete_expense"),
                       )
