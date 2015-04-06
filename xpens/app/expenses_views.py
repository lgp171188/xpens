from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
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
    EditPermissionOwnerUserOnlyMixin,
    GetDateRangesMixin,
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
                       GetDateRangesMixin,
                       ListView):
    context_object_name = "expenses"
    model = Expense
    template_name = "app/expenses/list.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        from_date_str = kwargs.get('from_date', None)
        to_date_str = kwargs.get('to_date', None)
        self.category_id = kwargs.get('category_id', None)
        self.from_date = self.to_date = None
        if from_date_str and to_date_str:
            try:
                self.from_date = datetime.strptime(from_date_str,
                                                   "%d-%m-%Y").date()
                self.to_date = datetime.strptime(to_date_str,
                                                 "%d-%m-%Y").date()
            except ValueError:
                if self.category_id:
                    return redirect(reverse_lazy('list_expenses_category',
                                                 kwargs={'category_id':
                                                         self.category_id}))
                else:
                    return redirect(reverse_lazy('list_expenses'))

        return super(ListExpensesView, self).dispatch(request,
                                                      *args,
                                                      **kwargs)

    def get_queryset(self):
        """Tweak the queryset to include only the expenses
        of the current user."""
        queryset = Expense.objects.filter(user=self.request.user)
        if self.from_date and self.to_date:
            queryset = queryset.filter(date__gte=self.from_date,
                                       date__lte=self.to_date)
        if self.category_id:
            category = get_object_or_404(Category, pk=self.category_id)
            queryset = queryset.filter(category=category)

        return queryset.order_by("-date", "-created")

    def get_context_data(self, **kwargs):
        context = super(ListExpensesView, self).get_context_data(**kwargs)
        context["category_list"] = Category.objects.filter(user=self.request.user)
        date_ranges = self._get_custom_range_dates()
        for value in date_ranges:
            context[value] = date_ranges[value].strftime("%d-%m-%Y")
        if self.category_id:
            context['category_id'] = self.category_id
            context['category_wise'] = True
            context['category_name'] = get_object_or_404(Category,
                                                         pk=self.kwargs['category_id']).name
        if self.from_date and self.to_date:
            context['date_range'] = True
            context['from_date'] = self.kwargs['from_date']
            context['to_date'] = self.kwargs['to_date']
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
