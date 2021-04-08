from django.db import models


class Company(models.Model):
    name = models.CharField('Название', max_length=100)
    inn = models.CharField('ИНН', max_length=10, unique=True)
    legal_address = models.TextField('Юридический адрес')
    actual_address = models.TextField('Фактический адрес', blank=True)
    phone = models.CharField('Телефон', max_length=15)
    email = models.EmailField(blank=True)
    # director: Admin = models.OneToOneField(Admin, on_delete=models.CASCADE)

    class Meta:
        db_table = 'companies'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f'Company {self.name}'


# to add "is active" field
class Route(models.Model):
    name = models.CharField('Название маршрута', max_length=10)
    begin = models.CharField('Начальная станиция', max_length=50)
    end = models.CharField('Конечная станция', max_length=50)
    stations = models.TextField('Станции', blank=True)

    class Meta:
        db_table = 'routes'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f'Route {self.name}'
