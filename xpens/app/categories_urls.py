from django.conf.urls import patterns, url

from .categories_views import (
    NewCategoryView,
    ListCategoriesView,
    UpdateCategoryView,
    DeleteCategoryView
)

urlpatterns = patterns('',
                       url(r'^$', ListCategoriesView.as_view(),
                           name="list_categories"),
                       url(r'^new/$', NewCategoryView.as_view(),
                           name="new_category"),
                       url(r'^(?P<pk>\d+)/update/$',
                           UpdateCategoryView.as_view(),
                           name="update_category"),
                       url(r'^(?P<pk>\d+)/delete/$',
                           DeleteCategoryView.as_view(),
                           name="delete_category"),
                       )
