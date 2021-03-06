from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.views.generic import (
    View,
    ListView,
    RedirectView
)

from django.contrib.auth.views import login as auth_login

from .models import Expense
from .mixins import LoginRequiredMixin


class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('home'))
        else:
            if settings.REGISTRATION_ENABLED:
                kwargs['registration_enabled'] = True
            return auth_login(request, *args, **kwargs)


class HomeView(LoginRequiredMixin,
               RedirectView):
    permanent = False
    url = reverse_lazy('overview')


class OverviewView(LoginRequiredMixin,
                   ListView):
    context_object_name = "expenses"
    model = Expense
    template_name = "app/overview.html"

    def get_queryset(self):
        return Expense.objects.most_recent_expenses_by_user(self.request.user)

    def _get_chart_data(self):
        expenses = Expense.objects.by_user_in_current_month(self.request.user)
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
                "height": "400",
                "width": "600",
                "x_is_date": False,
                "x_axis_format": '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            },
        }

        return data

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        data = self._get_chart_data()
        context['data'] = data
        context['total'] = sum(data['chartdata']['y1'])
        return context
