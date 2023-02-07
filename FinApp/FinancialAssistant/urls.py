from django.urls import path
from . import views

app_name = 'FinancialAssistant'
urlpatterns = [
    path('', views.index, name='index'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('new_category/', views.CategoryCreateView.as_view(), name='category_form'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/edit/<int:pk>/', views.UpdateEditView.as_view(), name='category_update'),
]
