from django.db import models
from Survey.models import Survey
from Auth.models import Admin, Mechanic, Car, Driver


class Tag(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Tag {self.name}'


class TypeRepair(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'types_repair'
        verbose_name = 'Тип ремонта'
        verbose_name_plural = 'Типы ремонтов'

    def __str__(self):
        return f'TypeRepair {self.name}'


class RepairRequest(models.Model):
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    info = models.TextField('Информация')
    completed = models.BooleanField('Обработан?', default=False)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='requests_repairs')
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        db_table = 'repair_requests'
        verbose_name = 'Запрос на ремонт'
        verbose_name_plural = 'Запросы на ремонт'

    def __str__(self):
        return f'RRequest date {self.date} car {self.car.user.username}'


class Repair(models.Model):
    info = models.TextField('Информация')
    date = models.DateTimeField('Дата', auto_now_add=True)
    request: RepairRequest = models.ForeignKey(RepairRequest, on_delete=models.CASCADE, null=True)
    mechanic: Mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    types_repair = models.ManyToManyField(TypeRepair)
    current_mileage = models.PositiveIntegerField('Пробег (км). Текущее показание адометра', default=0)

    class Meta:
        db_table = 'repairs'
        verbose_name = 'Ремонт'
        verbose_name_plural = 'Ремонты'

    def __str__(self):
        return f'Repair date {self.date} car {self.car.user.username}'
