from django.urls import path
from . import views

app_name = 'FinancialAssistant'
urlpatterns = [
    path('', views.index, name='index'),
    path('user_settings/', views.user_settings, name='user_settings'),

    path('new_family_budget/', views.FamilyBudgetCreateView.as_view(), name='new_family_budget'),
    path('family_budget/edit/<int:pk>/', views.FamilyBudgetUpdateView.as_view(), name='edit_family_budget'),

    path('new_category/', views.CategoryCreateView.as_view(), name='category_form'),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('new_currency/', views.CurrencyCreateView.as_view(), name='currency_form'),
    path('new_currency/edit/<int:pk>/', views.CurrencyUpdateView.as_view(), name='currency_update'),
    path('new_currency/<int:pk>/', views.CurrencyDetailView.as_view(), name='currency_detail'),

    path('edit_user/edit/<int:pk>/', views.UserUpdateView.as_view(), name='edit_user'),

    path('app_user_settings/edit/<int:pk>/', views.AppUserUpdateView.as_view(), name='app_user'),
]
