from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import UserCreationForm

class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Account created successfully. Please login to continue"
    template_name = "user_mgmt/register.html"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(RegistrationView, self).form_valid(form)
