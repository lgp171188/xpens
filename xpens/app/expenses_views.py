from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import (
    Expense,
    Category
)
from .forms import NewExpenseForm
from .mixins import (
    LoginRequiredMixin,
    SetCurrentUserInFormMixin,
    EditPermissionOwnerUserOnlyMixin
)


class NewExpenseView(LoginRequiredMixin,
                     SetCurrentUserInFormMixin,
                     CreateView):
    form_class = NewExpenseForm
    template_name = "app/expenses/new.html"
    success_url = reverse_lazy('list_expenses')
    success_message = "New expense successfully added"

    def get_form(self, form_class):
        form = super(NewExpenseView, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form


class ListExpensesView(LoginRequiredMixin,
                       ListView):
    context_object_name = "expenses"
    model = Expense
    template_name = "app/expenses/list.html"
    paginate_by = 10

    def get_queryset(self):
        """Tweak the queryset to include only the expenses
        of the current user."""
        queryset = Expense.objects.filter(user=self.request.user)
        return queryset.order_by("-date", "-created")

    def get_context_data(self, **kwargs):
        context = super(ListExpensesView, self).get_context_data(**kwargs)
        context["category_list"] = Category.objects.filter(user=self.request.user)
        return context


class ListCategoryExpensesView(ListExpensesView):

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, pk=category_id)
        queryset = Expense.objects.filter(category=category)
        return queryset.order_by("-date", "-created")

    def get_context_data(self, **kwargs):
        context = super(ListCategoryExpensesView, self).get_context_data(**kwargs)
        context['category_wise'] = True
        context['category_name'] = get_object_or_404(Category, pk=self.kwargs['category_id']).name
        return context


class UpdateExpenseView(LoginRequiredMixin,
                        EditPermissionOwnerUserOnlyMixin,
                        SetCurrentUserInFormMixin,
                        UpdateView):
    model = Expense
    form_class = NewExpenseForm
    template_name = "app/expenses/update.html"
    success_url = reverse_lazy('list_expenses')
    success_message = "Expense updated successfully"

    def get_form(self, form_class):
        form = super(UpdateExpenseView, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form


class DeleteExpenseView(LoginRequiredMixin,
                        EditPermissionOwnerUserOnlyMixin,
                        DeleteView):
    model = Expense
    template_name = "app/expenses/delete_confirm.html"
    success_url = reverse_lazy('list_expenses')


class SearchExpenseView(ListExpensesView):
    template_name = "app/expenses/search.html"

    def get_queryset(self):
        queryset = super(SearchExpenseView, self).get_queryset()
        search_value = self.request.GET.get('q', None)

        if search_value:
            queryset = queryset.filter(description__icontains=search_value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchExpenseView, self).get_context_data(**kwargs)
        if "category_list" in context:
            del context["category_list"]
        context['search_value'] = self.request.GET.get('q', '')
        return context
