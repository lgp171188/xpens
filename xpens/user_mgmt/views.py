from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from app.views import LoginRequiredMixin

from .forms import UserCreationForm


class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Account created successfully. Please login to continue"
    template_name = "user_mgmt/register.html"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(RegistrationView, self).form_valid(form)


class PasswordChangeView(LoginRequiredMixin,
                         FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('logout')
    success_message = "Password changed successfully"
    template_name = "user_mgmt/password_change.html"

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['user'] = self.request.user
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())
