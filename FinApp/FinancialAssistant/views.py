from django.shortcuts import render


def index(request):
    """Домашняя страница приложения."""
    return render(request=request, template_name='FinancialAssistant/index.html')
