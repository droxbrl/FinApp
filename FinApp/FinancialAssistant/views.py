from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView
from .models import User, Category, Currency, get_app_user, AppUser, Family
from .forms import UserSettingsForm, CreateFamilyBudgetForm, UserChangeCustomForm


def index(request):
    """Домашняя страница приложения."""
    return render(request=request, template_name='FinancialAssistant/index.html')


class CategoryCreateView(CreateView):
    """Вью создания категории."""
    model = Category
    fields = ['name', ]
    success_url = reverse_lazy('FinancialAssistant:user_settings')

    def form_valid(self, form):
        """Для подстановки user's."""
        form.instance.user = self.request.user
        return super(CategoryCreateView, self).form_valid(form)


class CategoryDetailView(DetailView):
    """Вью просмотра категории."""
    model = Category


class CategoryUpdateView(UpdateView):
    """Вью редактирования категории."""
    model = Category
    template_name = 'FinancialAssistant/category_update.html'
    fields = ['name', ]


class CurrencyCreateView(CreateView):
    """Вью создания категории."""
    model = Currency
    fields = ['code', 'num', 'name']
    success_url = reverse_lazy('FinancialAssistant:user_settings')

    def form_valid(self, form):
        """Для подстановки user's."""
        form.instance.user = self.request.user
        return super(CurrencyCreateView, self).form_valid(form)


class CurrencyDetailView(DetailView):
    """Вью просмотра категории."""
    model = Currency


class CurrencyUpdateView(UpdateView):
    """Вью редактирования категории."""
    model = Currency
    template_name = 'FinancialAssistant/currency_update.html'
    fields = ['code', 'num', 'name']


def check_owner(user, owner):
    """Проверяет текущего пользователя и "владельца" записи модели
        если они не совпадают - вызывает код 404."""
    if owner == user:
        pass
    else:
        raise Http404


class FamilyBudgetCreateView(CreateView):
    """Вью добавления семейного учета."""
    model = Family
    form_class = CreateFamilyBudgetForm
    template_name = 'FinancialAssistant/family_budget.html'
    success_url = reverse_lazy('FinancialAssistant:user_settings')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.members_to_update = []

    def form_valid(self, form):
        owner = get_app_user(user=self.request.user)
        for member in form.cleaned_data['members']:
            if member == owner:
                member.main_family_budget = True
            member.use_family_budget = True
            self.members_to_update.append(member)

        form.save()
        return super(FamilyBudgetCreateView, self).form_valid(form)

    def get_success_url(self):
        for member in self.members_to_update:
            member.family = self.object
            member.save()
        return super(FamilyBudgetCreateView, self).get_success_url()


class FamilyBudgetUpdateView(UpdateView):
    """Вью редактирования семейного учета."""
    model = Family
    form_class = CreateFamilyBudgetForm
    template_name = 'FinancialAssistant/family_budget_update.html'
    success_url = reverse_lazy('FinancialAssistant:user_settings')

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.members_to_update = []
    #
    # def form_valid(self, form):
    #     owner = get_app_user(user=self.request.user)
    #     for member in form.cleaned_data['members']:
    #         if member == owner:
    #             member.main_family_budget = True
    #         member.use_family_budget = True
    #         self.members_to_update.append(member)
    #
    #     form.save()
    #     return super(FamilyBudgetUpdateView, self).form_valid(form)
    #
    # def get_success_url(self):
    #     for member in self.members_to_update:
    #         member.family = self.object
    #         member.save()
    #     return super(FamilyBudgetUpdateView, self).get_success_url()


def user_settings(request):
    """Вью пользовательских настроек."""

    user_settings_data = User.objects.filter(id=request.user.id).first()
    form_user_settings = UserSettingsForm(instance=user_settings_data)
    category_data = Category.objects.filter(user=request.user)
    currency_data = Currency.objects.filter(user=request.user)
    app_user = get_app_user(user=request.user)
    family_data = {}
    if app_user.family:
        family_members = []
        for member in AppUser.objects.filter(family=app_user.family):
            if member != app_user:
                family_members.append(member)
        family_data = {'family': app_user.family,
                       'family_members_names': family_members}

    context = {'form_user_settings': form_user_settings,
               'family_data': family_data,
               'category_data': category_data,
               'currency_data': currency_data,
               'app_user': app_user}

    return render(context=context, request=request, template_name='FinancialAssistant/user_settings.html')


# @login_required
class UserUpdateView(UpdateView):
    """Вью редактирования пользователя."""
    model = User
    template_name = 'FinancialAssistant/user_form.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('FinancialAssistant:user_settings')


class AppUserUpdateView(UpdateView):
    """Вью редактирования доп настроек пользователя."""
    model = AppUser
    template_name = 'FinancialAssistant/app_user.html'
    fields = ['tg_id',
              'use_family_budget',
              'main_family_budget',
              ]
    success_url = reverse_lazy('FinancialAssistant:user_settings')
