from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from Core.models import Company


class User(AbstractUser):
    roles = [
        ('D', 'Driver'),
        ('M', 'Mechanic'),
        ('A', 'Admin'),
        ('C', 'Car')
    ]

    third_name = models.CharField('Отчество', blank=True, null=True,
                                  max_length=100)
    role = models.CharField('Роль', choices=roles, max_length=10)
    company: Company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'users'


class Admin(models.Model):
    user: User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'admins'

    def __str__(self):
        return f'Admin {self.user.username}'

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super().delete(using, keep_parents)


class Driver(models.Model):
    license = models.CharField('ВУ', max_length=10)
    others = models.TextField('Другое', blank=True)
    date_license = models.DateField()
    user: User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # main_route

    class Meta:
        db_table = 'drivers'
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return f'Driver {self.user.username}'

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super().delete(using, keep_parents)


class Mechanic(models.Model):
    others = models.TextField('Другое', blank=True)
    date_med_card = models.DateField()
    user: User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mechanics'
        verbose_name = 'Механик'
        verbose_name_plural = 'Механики'

    def __str__(self):
        return f'Mechanic {self.user.username}'

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super().delete(using, keep_parents)


class Car(models.Model):
    types_engine = [
        ('P', 'Бензин'),
        ('G', 'Газовый'),
        ('D', 'Дизель'),
        ('E', 'Электрический'),
    ]
    env_classes = [
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ]

    mark = models.CharField('Марка', max_length=255)
    model = models.CharField('Модель', max_length=255)
    vin = models.CharField('VIN', max_length=17)
    year = models.DateField('Год')
    color = models.CharField('Цвет', max_length=20, blank=True)
    ctc = models.CharField('СТС', max_length=12, blank=True)
    ptc = models.CharField('ПТС', max_length=15, blank=True)
    owner = models.CharField('Собственник', max_length=100, blank=True, null=True)
    mileage = models.PositiveIntegerField('Пробег (км). Текущее показание адометра')
    to1 = models.PositiveIntegerField('ТО1', blank=True, null=True)
    to2 = models.PositiveIntegerField('ТО2', blank=True, null=True)
    engine = models.CharField('Двигатель', blank=True, max_length=50, null=True)
    power_engine = models.CharField('Мощность двигателя', max_length=10, blank=True, null=True)
    type_engine = models.CharField('Тип двигателя', choices=types_engine, max_length=5)
    env_class = models.CharField('Экологический класс', choices=env_classes, max_length=5)
    osago = models.CharField('Номер полиса ОСАГО', max_length=50, blank=True, null=True)
    osago_validity = models.DateField('Срок действия ОСАГО', blank=True, null=True)
    diagnostic_card = models.CharField('Диагностическая карта', max_length=50, blank=True, null=True)
    diagnostic_card_validity = models.DateField('Срок действия техосмотра', blank=True, null=True)
    user: User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='car')

    class Meta:
        db_table = 'cars'
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f'Car {self.user.username} Company {self.user.company.name}'

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super().delete(using, keep_parents)

