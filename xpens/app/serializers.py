from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'created', 'modified', 'user',)


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        super(ExpenseSerializer, self).__init__(*args, **kwargs)
        current_user = kwargs['context']['request'].user
        self.fields['category'].queryset = Category.objects.filter(user=current_user)

    class Meta:
        model = Expense
        fields = ('id', 'date', 'amount', 'category', 'description', 'created', 'modified', 'user',)
