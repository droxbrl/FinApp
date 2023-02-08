from django.contrib import admin
from .models import AppUser, Family, Currency, Category, CashFlow, OperationType

admin.site.register(AppUser)
admin.site.register(Family)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(CashFlow)
admin.site.register(OperationType)
