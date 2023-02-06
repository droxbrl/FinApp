from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegisterForm


def register(request):
    """Вью регистрации нового пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('FinancialAssistant:index')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request=request, template_name='users/register.html', context=context)
