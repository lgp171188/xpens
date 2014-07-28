from datetime import date
from django.db.models import Sum
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView, RedirectView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import *
from .forms import *

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

class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('home'))
        else:
            return auth_login(request, *args, **kwargs)

class HomeView(LoginRequiredMixin,
               RedirectView):
    url = reverse_lazy('overview')

class ListExpensesView(LoginRequiredMixin,
                       ListView):
    context_object_name = "expenses"
    model = Expense
    template_name = "app/list_expenses.html"
    paginate_by = 10

    def get_queryset(self):
        """Tweak the queryset to include only the expenses
        of the current user."""
        queryset = Expense.objects.filter(user=self.request.user)
        return queryset

class NewExpenseView(LoginRequiredMixin,
                     SetCurrentUserInFormMixin,
                     CreateView):
    form_class = NewExpenseForm
    template_name = "app/new_expense.html"
    success_url = reverse_lazy('list_expenses')
    success_message = "New expense successfully added"

    def get_form(self, form_class):
        form = super(NewExpenseView, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form

class ListCategoriesView(LoginRequiredMixin, ListView):
    context_object_name = "categories"
    model = Category
    template_name = "app/list_categories.html"
    paginate_by = 10

    def get_queryset(self):
        """Tweak the queryset to include only the categories
        of the current user."""
        queryset = Category.objects.filter(user=self.request.user)
        return queryset

class NewCategoryView(LoginRequiredMixin,
                      SetCurrentUserInFormMixin,
                      CreateView):
    form_class = NewCategoryForm
    template_name = "app/new_category.html"
    success_url = reverse_lazy('list_categories')
    success_message = "New Category successfully added"

class UpdateExpenseView(LoginRequiredMixin,
                        EditPermissionOwnerUserOnlyMixin,
                        SetCurrentUserInFormMixin,
                        UpdateView):
    model = Expense
    form_class = NewExpenseForm
    template_name = "app/update_expense.html"
    success_url = reverse_lazy('list_expenses')
    success_message = "Expense updated successfully"

    def get_form(self, form_class):
        form = super(UpdateExpenseView, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form

class UpdateCategoryView(LoginRequiredMixin,
                         EditPermissionOwnerUserOnlyMixin,
                         SetCurrentUserInFormMixin,
                         UpdateView):
    model = Category
    form_class = NewCategoryForm
    template_name = "app/update_category.html"
    success_url = reverse_lazy('list_categories')
    success_message = "Category updated successfully"

    def get_object(self, queryset=None):
        category = super(UpdateCategoryView, self).get_object()
        if category.user != self.request.user:
            raise PermissionDenied
        return category

class DeleteExpenseView(LoginRequiredMixin,
                        EditPermissionOwnerUserOnlyMixin,
                        DeleteView):
    model = Expense
    template_name = "app/delete_expense_confirm.html"
    success_url = reverse_lazy('list_expenses')

class DeleteCategoryView(LoginRequiredMixin,
                        EditPermissionOwnerUserOnlyMixin,
                        DeleteView):
    model = Category
    template_name = "app/delete_category_confirm.html"
    success_url = reverse_lazy('list_categories')

class OverviewView(LoginRequiredMixin,
                       ListView):
    context_object_name = "expenses"
    model = Expense
    template_name = "app/overview.html"

    def get_queryset(self):
        """Tweak the queryset to include only the expenses
        of the current user."""
        queryset = Expense.objects.filter(user=self.request.user).order_by("-date")[:5]
        return queryset

    def _get_chart_data(self):
        today = date.today()
        current_month_beginning = date(today.year, today.month, 1)
        expenses = Expense.objects.filter(date__gte=current_month_beginning)
        categories = [category['category__name'] for category in expenses.values('category__name').distinct()]
        aggregate = []
        for category in categories:
            aggregate.append(int(expenses.filter(category__name=category).aggregate(Sum('amount'))['amount__sum']))
        data = {
            'charttype' : 'pieChart',
            'chartdata' : {'x': categories, 'y': aggregate},
            'chartcontainer' : 'piechart_container',
            'extra' : {
                "height" : "400",
                "width" : "600",
            },
        }
        return data

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        context['data'] = self._get_chart_data()
        return context
