from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import generics

from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer


class CategoryList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        serializer_context = super(CategoryList, self).get_serializer_context()
        serializer_context['request'] = self.request
        return serializer_context

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_object(self):
        try:
            current_user_categories = Category.objects.filter(user=self.request.user)
            return current_user_categories.get(pk=self.kwargs['pk'])
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExpenseList(generics.ListAPIView,
                  generics.CreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        serializer_context = super(ExpenseList, self).get_serializer_context()
        serializer_context['request'] = self.request
        return serializer_context

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExpenseDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpenseSerializer

    def get_object(self):
        try:
            current_user_expenses = Expense.objects.filter(user=self.request.user)
            return current_user_expenses.get(pk=self.kwargs['pk'])
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
