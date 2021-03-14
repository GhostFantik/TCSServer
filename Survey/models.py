from django.db import models
from Core.models import Route
from Auth.models import Driver, Car


class Survey(models.Model):
    date = models.DateField('Дата')
    start_time = models.DateTimeField('Время начала маршрута')
    end_time = models.DateTimeField('Время окончания маршрута')
    money = models.PositiveIntegerField('Наличный расчет')
    red = models.PositiveIntegerField('Красный валидатор')
    black = models.PositiveIntegerField('Чёрный валидатор')
    km = models.PositiveIntegerField('Пробег (В РАЗРАБОТКЕ)')
    car: Car = models.ForeignKey(Car, on_delete=models.SET_NULL, verbose_name='Транспорт',
                                 null=True)
    driver: Driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, verbose_name='Водитель',
                                       null=True)
    route: Route = models.ForeignKey(Route, on_delete=models.SET_NULL, verbose_name='Маршрут',
                                     null=True)

    class Meta:
        db_table = 'surveys'
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'

    def __str__(self):
        return f'Survey date {self.date}'


