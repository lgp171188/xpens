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
