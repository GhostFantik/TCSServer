from rest_framework import serializers
from rest_framework.exceptions import NotFound
from djoser.compat import get_user_email, get_user_email_field_name
from django.conf import settings
from Auth.models import User, Car, Mechanic, Admin, Driver
from Core.models import Company


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'third_name', 'role', 'company')

        read_only_fields = ('username',)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)


class BaseUserRoleSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для Mechanic, Admin и Car. Реализует создания нового юзера для этих ролей
    """
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    username = serializers.CharField(max_length=10, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)
    company_name = serializers.CharField(max_length=100, write_only=True)
    company = serializers.CharField(max_length=100, read_only=True, source='user.company.name')

    def create_user(self, validated_data) -> User:
        try:
            username = validated_data.pop('username')
            if User.objects.filter(username=username).exists():
                raise NotFound('This user already exists!')
            u: User = User(username=username)
            u.set_password(validated_data.pop('password'))
            company: Company = Company.objects.get(name=validated_data.pop('company_name'))
            u.company = company
            u.save()
            return u
        except Company.DoesNotExist:
            raise NotFound('Company does not exist!')

    def update(self, instance, validated_data):
        data_user = validated_data.pop('user', None)
        if data_user:
            instance.user.first_name = data_user.pop('first_name', instance.user.first_name)
            instance.user.last_name = data_user.pop('last_name', instance.user.last_name)
            instance.user.third_name = data_user.pop('third_name', instance.user.third_name)
            instance.user.save()
        super().update(instance, validated_data)
        return instance


class CarSerializer(BaseUserRoleSerializer):
    """
    Сериализатор для Car
    """

    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        u: User = super().create_user(validated_data)
        u.role = 'C'
        u.save()
        car: Car = Car.objects.create(user=u, **validated_data)
        return car


class MechanicSerializer(BaseUserRoleSerializer):
    """
    Сериализатор для Mechanic
    """
    first_name = serializers.CharField(max_length=100, source='user.first_name')
    last_name = serializers.CharField(max_length=100, source='user.last_name')
    third_name = serializers.CharField(max_length=100, source='user.third_name', allow_blank=True)

    class Meta:
        model = Mechanic
        fields = '__all__'

    def create(self, validated_data):
        u: User = super().create_user(validated_data)
        du: dict = validated_data.pop('user')
        u.first_name = du.get('first_name', '')
        u.last_name = du.get('last_name', '')
        u.third_name = du.get('third_name', '')
        u.role = 'M'
        u.save()
        mechanic: Mechanic = Mechanic.objects.create(user=u, **validated_data)
        return mechanic


class AdminSerializer(BaseUserRoleSerializer):
    """
    Сериализатор для Admin
    """
    first_name = serializers.CharField(max_length=100, source='user.first_name')
    last_name = serializers.CharField(max_length=100, source='user.last_name')
    third_name = serializers.CharField(max_length=100, source='user.third_name', allow_blank=True)

    class Meta:
        model = Admin
        fields = '__all__'

    def create(self, validated_data):
        u: User = super().create_user(validated_data)
        du: dict = validated_data.pop('user')
        u.first_name = du.get('first_name', '')
        u.last_name = du.get('last_name', '')
        u.third_name = du.get('third_name', '')
        u.role = 'A'
        u.save()
        admin: Admin = Admin.objects.create(user=u, **validated_data)
        return admin


class DriverSerializer(BaseUserRoleSerializer):
    """
    Сериализатор для Driver
    """
    first_name = serializers.CharField(max_length=100, source='user.first_name')
    last_name = serializers.CharField(max_length=100, source='user.last_name')
    third_name = serializers.CharField(max_length=100, source='user.third_name', allow_blank=True)

    class Meta:
        model = Driver
        fields = '__all__'

    def create(self, validated_data):
        u: User = super().create_user(validated_data)
        du: dict = validated_data.pop('user')
        u.first_name = du.get('first_name', '')
        u.last_name = du.get('last_name', '')
        u.third_name = du.get('third_name', '')
        u.role = 'D'
        u.save()
        driver: Driver = Driver.objects.create(user=u, **validated_data)
        return driver
