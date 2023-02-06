from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    """Вью регистрации нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('FinancialAssistant:index')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request=request, template_name='users/register.html', context=context)
