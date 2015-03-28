from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from .mixins import (
    LoginRequiredMixin,
    SetCurrentUserInFormMixin,
    EditPermissionOwnerUserOnlyMixin
)
from .models import Category
from .forms import NewCategoryForm


class ListCategoriesView(LoginRequiredMixin, ListView):
    context_object_name = "categories"
    model = Category
    template_name = "app/categories/list.html"
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
    template_name = "app/categories/new.html"
    success_url = reverse_lazy('list_categories')
    success_message = "New Category successfully added"

    def get_form_kwargs(self, *args, **kwargs):
        return dict(super(NewCategoryView, self).get_form_kwargs(*args, **kwargs),
                    user=self.request.user)


class UpdateCategoryView(LoginRequiredMixin,
                         EditPermissionOwnerUserOnlyMixin,
                         SetCurrentUserInFormMixin,
                         UpdateView):
    model = Category
    form_class = NewCategoryForm
    template_name = "app/categories/update.html"
    success_url = reverse_lazy('list_categories')
    success_message = "Category updated successfully"

    def get_object(self, queryset=None):
        category = super(UpdateCategoryView, self).get_object()
        if category.user != self.request.user:
            raise PermissionDenied
        return category

    def get_form_kwargs(self, *args, **kwargs):
        return dict(super(UpdateCategoryView, self).get_form_kwargs(*args, **kwargs),
                    user=self.request.user)


class DeleteCategoryView(LoginRequiredMixin,
                         EditPermissionOwnerUserOnlyMixin,
                         DeleteView):
    model = Category
    template_name = "app/categories/delete_confirm.html"
    success_url = reverse_lazy('list_categories')
