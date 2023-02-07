from django.urls import path
from . import views

app_name = 'FinancialAssistant'
urlpatterns = [
    path('', views.index, name='index'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('new_category/', views.CategoryCreateView.as_view(), name='category_form'),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('new_currency/', views.CurrencyCreateView.as_view(), name='currency_form'),
    path('new_currency/edit/<int:pk>/', views.CurrencyUpdateView.as_view(), name='currency_update'),
    path('new_currency/<int:pk>/', views.CurrencyDetailView.as_view(), name='currency_detail'),
]
