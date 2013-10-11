from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView, CreateView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from .models import *
from .forms import *
class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('home'))
        else:
            return auth_login(request, *args, **kwargs)

class HomeView(TemplateView):
    template_name = "app/index.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

class ListExpensesView(ListView):
    context_object_name = "expenses"
    model = Expense
    template_name = "app/list_expenses.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListExpensesView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Tweak the queryset to include only the expenses of the current user."""
        queryset = Expense.objects.filter(user=self.request.user)
        return queryset

class NewExpenseView(CreateView):
    form_class = NewExpenseForm
    template_name = "app/new_expense.html"
    success_url = reverse_lazy('list_expenses')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewExpenseView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class ListCategoriesView(ListView):
    context_object_name = "categories"
    model = Category
    template_name = "app/list_categories.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListCategoriesView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Tweak the queryset to include only the categories of the current user."""
        queryset = Category.objects.filter(user=self.request.user)
        return queryset

class NewCategoryView(CreateView):
    form_class = NewCategoryForm
    template_name = "app/new_category.html"
    success_url = reverse_lazy('list_categories')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewCategoryView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())
