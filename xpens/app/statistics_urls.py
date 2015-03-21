from django.conf.urls import patterns, url

from .statistics_views import StatisticsView

urlpatterns = patterns('',
                       url(r'^categories/(?P<from_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/to/(?P<to_date>[0-9]{2}-[0-9]{2}-[0-9]{4})/$',
                           StatisticsView.as_view(),
                           name="statistics_custom"),
                       url(r'^categories/$',
                           StatisticsView.as_view(),
                           name="statistics"),
)
