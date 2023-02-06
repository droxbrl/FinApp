from django.urls import path
from . import views

app_name = 'FinancialAssistant'
urlpatterns = [
    path('', views.index, name='index'),
]
