from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('url', 'name', 'description', 'created', 'modified', 'user', 'expenses')


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        super(ExpenseSerializer, self).__init__(*args, **kwargs)
        current_user = kwargs['context']['request'].user
        self.fields['category'].queryset = Category.objects.filter(user=current_user)

    class Meta:
        model = Expense
        fields = ('url', 'date', 'amount', 'category', 'description', 'created', 'modified', 'user',)
