from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views

urlpatterns = [
    url(r'^categories/$',
        api_views.CategoryList.as_view(),
        name="api_list_categories",
    ),

    url(r'^category/(?P<pk>[0-9]+)/$',
        api_views.CategoryDetail.as_view(),
        name="api_category_detail",
    ),
    url(r'^expenses/$',
        api_views.ExpenseList.as_view(),
        name="api_list_expenses",
    ),
    url(r'^expense/(?P<pk>[0-9]+)/$',
        api_views.ExpenseDetail.as_view(),
        name="api_expense_detail",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
