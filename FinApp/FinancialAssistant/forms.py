from typing import Optional
from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import User, Family, Currency, Category, AppUser


class CreateFamilyBudgetForm(forms.ModelForm):
    """Форма пользователя приложения."""

    class Meta:
        model = Family
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter family name'})
        }
        labels = {
            "name": "Family name",
        }

    members = forms.ModelMultipleChoiceField(
        queryset=AppUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Mark family members:'
    )

    field_order = ['name', 'members']


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


class CategoryForm(forms.ModelForm):
    """Форма настроек категорий учета."""

    class Meta:
        model = Category
        fields = ('name',)

        widgets = {

        }


class CurrencyForm(forms.ModelForm):
    """Форма настроек семейного учета."""

    class Meta:
        model = Currency
        fields = ('name', 'code', 'num')

        widgets = {

        }


class UserChangeCustomForm(UserChangeForm):
    """Форма изменения пользовательских настроек."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


