from django import forms
from .models import User, OverallBudget, Currency, Category


class UserSettingsForm(forms.ModelForm):
    """Форма настроек пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(UserSettingsForm, self).__init__(*args, **kwargs)
    #     if 'initial' in kwargs:
    #         initial = kwargs.get('initial')
    #         self.fields['user'].queryset = User.objects.filter(id=initial.get('user').id)
    #         self.fields['family'].queryset = OverallBudget.objects.filter(users=initial.get('user'))
    #         self.fields['currencies'].queryset = Currency.objects.filter(user=initial.get('user'))
    #         self.fields['categories'].queryset = Category.objects.filter(user=initial.get('user'))


class OverallBudgetSettings(forms.ModelForm):
    """Форма настроек семейного учета."""

    class Meta:
        model = OverallBudget
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'users': forms.Select(attrs={'readonly': 'readonly'}),
        }


class CategoryForm(forms.ModelForm):
    """Форма настроек катерогий учета."""

    class Meta:
        model = Category
        fields = ('name',)

        widgets = {

        }


class CategoryForm(forms.ModelForm):
    """Форма настроек семейного учета."""

    class Meta:
        model = Currency
        fields = ('name', 'code', 'num')

        widgets = {

        }
