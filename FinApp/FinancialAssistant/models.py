"""Модели базы данных."""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import datetime


class TelegramUser(models.Model):
    """Модель для связи юзеров тг-бота и веб-версии."""
    tg_id = models.BigIntegerField(verbose_name='telegram user id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Telegram user <telegram id: {self.tg_id},  user: {self.user.__str__()}>'


class OverallBudget(models.Model):
    """Модель общего (семейного) учета."""
    name = models.CharField(max_length=120)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Overall budget <name: {self.name}>'


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
        return f'{self.name} ({self.code})'

    def get_absolute_url(self):
        return reverse('FinancialAssistant:currency_detail', args=(str(self.id)))



class Category(models.Model):
    """Модель категории."""
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name="category_unique")
        ]

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('FinancialAssistant:category_detail', args=(str(self.id)))


class OperationType(models.Model):
    """Модель вида операций (приход/расход)"""
    type = models.CharField(max_length=10)
    check_minus = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'Operation type <type: {self.type}, check_minus {self.check_minus}>'


class CashFlow(models.Model):
    """Модель учета денежных потоков. Основная таблица, все отчеты готовим по данным этой таблицы."""
    date_time = models.DateTimeField(default=datetime.now)
    amount = models.FloatField()
    type = models.ForeignKey(OperationType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    family = models.ForeignKey(OverallBudget, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Перегружаю метод для проверки знака перед записью. Для расхода нужно добавлять '-', если его еще нет"""
        if self.type.check_minus and self.amount > 0:
            self.amount *= -1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Cash flow <amount: {self.amount}, type: {self.type}, ' \
               f'category: {self.category}, currency: {self.currency}, added: {self.date_time}>'


class UserSetting(models.Model):
    """Хранит настройки пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(OverallBudget, null=True, on_delete=models.SET_NULL, blank=True)
    currencies = models.ManyToManyField(Currency, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        if self.user.first_name:
            user_name = self.user.first_name.capitalize()
        else:
            user_name = str(self.user).capitalize()
        return f'<{user_name} settings: family: {self.family}, categories: {self.categories}, ' \
               f'currencies: {self.currencies}>'
