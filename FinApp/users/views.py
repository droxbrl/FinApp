from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from FinancialAssistant.forms import AppUser
from django.shortcuts import render, redirect


def register(request):
    """Регистрирует нового пользователя"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            save_app_user_data(new_user)
            login(request, new_user)
            return redirect('FinancialAssistant:index')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def save_app_user_data(new_user):
    """Связывает нового пользователя с моделью AppUser."""
    AppUser.objects.create(user=new_user)
