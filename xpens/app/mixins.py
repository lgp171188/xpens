from datetime import date

from dateutil.relativedelta import relativedelta

from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,
                                                        *args,
                                                        **kwargs)


class SetCurrentUserInFormMixin(object):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())


class EditPermissionOwnerUserOnlyMixin(object):

    def get_object(self, queryset=None):
        obj = super(EditPermissionOwnerUserOnlyMixin, self).get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj


class GetDateRangesMixin(object):

    def _get_custom_range_dates(self):
        dates = {}
        today = date.today()
        begin_curr_month = today.replace(day=1)
        dates["cm_f_date"] = begin_curr_month
        dates["today"] = today
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
