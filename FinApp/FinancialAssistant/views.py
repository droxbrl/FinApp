from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, CreateView
from .models import User, OverallBudget, Category, Currency
from .forms import UserSettingsForm, OverallBudgetSettings


def index(request):
    """Домашняя страница приложения."""
    return render(request=request, template_name='FinancialAssistant/index.html')


#
def user_settings(request):
    """Вью пользовательских настроек."""
    #     form = UserSettingsForm(instance=user_settings_data, initial={'user': request.user})
    #     form = UserSettingsForm(initial={'user': request.user})

    user_settings_data = User.objects.filter(id=request.user.id).first()
    form_user_settings = UserSettingsForm(instance=user_settings_data)

    overall_budget_data = OverallBudget.objects.filter(users=request.user).first()

    form_overall_budget_settings = OverallBudgetSettings(instance=overall_budget_data)

    category_data = Category.objects.filter(user=request.user)

    currency_data = Currency.objects.filter(user=request.user)

    context = {'form_user_settings': form_user_settings,
               'form_overall_budget_settings': form_overall_budget_settings,
               'category_data': category_data,
               'currency_data': currency_data}

    return render(context=context, request=request, template_name='FinancialAssistant/user_settings.html')


class CategoryCreateView(CreateView):
    """Вью создания категории."""
    model = Category
    fields = ['name', ]

    def form_valid(self, form):
        """Для подстановки user's."""
        form.instance.user = self.request.user
        return super(CategoryCreateView, self).form_valid(form)


class CategoryDetailView(DetailView):
    """Вью просмотра категории."""
    model = Category


class UpdateEditView(UpdateView):
    """Вью редактирования категории."""
    model = Category
    fields = ['name', ]


def check_owner(user, owner):
    """Проверяет текущего пользователя и "владельца" записи модели
        если они не совпадают - вызывает код 404."""
    if owner == user:
        pass
    else:
        raise Http404
