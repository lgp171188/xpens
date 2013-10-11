from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class SetCurrentUserInFormMixin(object):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())

class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('home'))
        else:
            return auth_login(request, *args, **kwargs)

class HomeView(TemplateView, LoginRequiredMixin):
    template_name = "app/index.html"

class ListExpensesView(LoginRequiredMixin, ListView):
    context_object_name = "expenses"
    model = Expense
    template_name = "app/list_expenses.html"

    def get_queryset(self):
        """Tweak the queryset to include only the expenses of the current user."""
        queryset = Expense.objects.filter(user=self.request.user)
        return queryset

class NewExpenseView(LoginRequiredMixin, SetCurrentUserInFormMixin, CreateView):
    form_class = NewExpenseForm
    template_name = "app/new_expense.html"
    success_url = reverse_lazy('list_expenses')
    success_message = "New expense successfully added"

class ListCategoriesView(LoginRequiredMixin, ListView):
    context_object_name = "categories"
    model = Category
    template_name = "app/list_categories.html"

    def get_queryset(self):
        """Tweak the queryset to include only the categories of the current user."""
        queryset = Category.objects.filter(user=self.request.user)
        return queryset

class NewCategoryView(LoginRequiredMixin, SetCurrentUserInFormMixin, CreateView):
    form_class = NewCategoryForm
    template_name = "app/new_category.html"
    success_url = reverse_lazy('list_categories')
    success_message = "New Category successfully added"

class UpdateExpenseView(LoginRequiredMixin, SetCurrentUserInFormMixin, UpdateView):
    model = Expense
    form_class = NewExpenseForm
    template_name = "app/update_expense.html"
    success_url = reverse_lazy('list_expenses')
    success_message = "Expense updated successfully"

class UpdateCategoryView(LoginRequiredMixin, SetCurrentUserInFormMixin, UpdateView):
    model = Category
    form_class = NewCategoryForm
    template_name = "app/update_category.html"
    success_url = reverse_lazy('list_categories')
    success_message = "Category updated successfully"
