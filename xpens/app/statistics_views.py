from datetime import date, datetime
import calendar

from dateutil.relativedelta import relativedelta

from django.db.models import Sum
from django.views.generic import TemplateView

from .models import Expense, Category
from .mixins import LoginRequiredMixin


class StatisticsView(LoginRequiredMixin,
                     TemplateView):
    template_name = "app/statistics.html"

    def _get_chart_data(self):
        from_date_str = self.kwargs.get('from_date', None)
        to_date_str = self.kwargs.get('to_date', None)
        if not from_date_str and not to_date_str:
            today = date.today()
            self.from_date = date(today.year, today.month, 1)
            self.to_date = today
        else:
            try:
                self.from_date = datetime.strptime(from_date_str, "%d-%m-%Y").date
                self.to_date = datetime.strptime(to_date_str, "%d-%m-%Y").date
            except ValueError:
                self.from_date = self.to_date = None
        expenses = Expense.objects.filter(user=self.request.user,
                                          date__gte=self.from_date,
                                          date__lte=self.to_date)
        categories = [category['category__name'] for category in expenses.values('category__name').distinct()]

        aggregate = []
        for category in categories:
            aggregate.append(int(expenses.filter(category__name=category).aggregate(Sum('amount'))['amount__sum']))
        data = {
            'charttype' : 'pieChart',
            'chartdata' : {'x': categories, 'y': aggregate},
            'chartcontainer' : 'piechart_container',
            'extra' : {
                'height' : "400",
            },
        }
        return data

    def _get_custom_range_dates(self):
        dates = {}
        today = date.today()
        begin_curr_month = today.replace(day=1)
        dates["pm_f_date"] = begin_curr_month - relativedelta(months=1)
        dates["pm_t_date"] = begin_curr_month - relativedelta(days=1)
        dates["cpm_f_date"] = dates["pm_f_date"]
        dates["cpm_t_date"] = today
        dates["six_f_date"] = begin_curr_month - relativedelta(months=6)
        dates["six_t_date"] = today
        dates["cy_f_date"] = date(today.year,
                                  1,
                                  1)
        dates["cy_t_date"] = today
        dates["py_f_date"] = date(today.year-1,
                                  1,
                                  1)
        dates["py_t_date"] = date(today.year-1,
                                  12,
                                  31)
        return dates

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        data = self._get_chart_data()
        context['data'] = data
        context['total'] = sum(data['chartdata']['y'])
        context['from_date'] = self.from_date
        context['to_date'] = self.to_date
        ranges = self._get_custom_range_dates()
        for k in ranges.keys():
            context[k] = ranges[k].strftime("%d-%m-%Y")
        return context
