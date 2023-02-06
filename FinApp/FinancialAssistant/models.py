from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import datetime


class TelegramUser(models.Model):
    """Модель для связи юзеров тг-бота и веб-версии."""
    tg_id = models.BigIntegerField(verbose_name='telegram user id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Telegram_user <telegram id: {self.tg_id},  user: {self.user.__str__()}>'


class OverallBudget(models.Model):
    """Модель общего (семейного) учета."""
    name = models.CharField(max_length=120)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Overall_budget <name: {self.name}>'


class Currency(models.Model):
    """Модель валюты."""
    code = models.CharField(max_length=3)
    num = models.IntegerField(validators=[MaxValueValidator(999)])
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'num', 'name', 'user'], name="currency_unique")
        ]

    def save(self, *args, **kwargs):
        """Перегружаю метод для форматирования кода и наименования валюты."""
        self.code = self.code.upper()
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Currency <code: {self.code}, num: {self.num}, name: {self.name}>'


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name="category_unique")
        ]

    def __str__(self):
        return f'Category <name: {self.name}>'


class OperationType(models.Model):
    """Модель вида операций (приход/расход)"""
    type = models.CharField(max_length=10)
    check_minus = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'Operation_type <type: {self.type}, check_minus {self.check_minus}>'


class CashFlow(models.Model):
    """Модель учета денежных потоков."""
    date_time = models.DateTimeField(default=datetime.now())
    amount = models.FloatField()
    type = models.ForeignKey(OperationType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Перегружаю метод для проверки знака перед записью. Для расхода нужно добавлять -"""
        if self.type.check_minus and self.amount > 0:
            self.amount *= -1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'CashFlow <amount: {self.amount}, type: {self.type}, ' \
               f'category: {self.category}, currency: {self.currency}, added: {self.date_time}>'
