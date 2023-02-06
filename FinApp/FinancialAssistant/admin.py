from django.contrib import admin
from .models import TelegramUser, OverallBudget, Currency, Category, CashFlow, OperationType

admin.site.register(TelegramUser)
admin.site.register(OverallBudget)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(CashFlow)
admin.site.register(OperationType)
