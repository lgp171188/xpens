from datetime import date, datetime

from django.db.models import Sum
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy

from .models import Expense
from .mixins import (
    LoginRequiredMixin,
    GetDateRangesMixin,
)


class StatisticsView(LoginRequiredMixin,
                     GetDateRangesMixin,
                     TemplateView):
    template_name = "app/statistics.html"

    def dispatch(self, request, *args, **kwargs):
        from_date_str = kwargs.get('from_date', None)
        to_date_str = kwargs.get('to_date', None)

        if from_date_str and to_date_str:
            try:
                datetime.strptime(from_date_str, "%d-%m-%Y")
                datetime.strptime(to_date_str, "%d-%m-%Y")
            except ValueError:
                return redirect(reverse_lazy('statistics'))
        return super(StatisticsView, self).dispatch(request,
                                                    *args,
                                                    **kwargs)

    def _set_date_range(self):
        from_date_str = self.kwargs.get('from_date', None)
        to_date_str = self.kwargs.get('to_date', None)
        if not from_date_str and not to_date_str:
            today = date.today()
            self.from_date = date(today.year, today.month, 1)
            self.to_date = today
        else:
            self.from_date = datetime.strptime(from_date_str, "%d-%m-%Y").date
            self.to_date = datetime.strptime(to_date_str, "%d-%m-%Y").date


    def _get_chart_data(self):
        self._set_date_range()
        expenses = Expense.objects.by_user_between_dates(self.request.user,
                                                         self.from_date,
                                                         self.to_date)
        categories = expenses.distinct_category_names()
        aggregate = expenses.category_wise_total_for(categories)
        data = {
            'charttype': 'pieChart',
            'chartdata': {
                'x': categories,
                'y1': aggregate,
                'extra1': {
                    'tooltip': {
                        'y_start': '',
                        'y_end': ''}
                }
            },
            'chartcontainer': 'piechart_container',
            'extra': {
                'height': "400",
            },
        }
        return data

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        data = self._get_chart_data()
        context['data'] = data
        context['total'] = sum(data['chartdata']['y1'])
        context['from_date'] = self.from_date
        context['to_date'] = self.to_date
        ranges = self._get_custom_range_dates()
        for k in ranges.keys():
            context[k] = ranges[k].strftime("%d-%m-%Y")
        return context
