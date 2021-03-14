from rest_framework import serializers
from rest_framework.exceptions import NotFound
from Survey.models import Survey
from Auth.models import Driver, Car
from Core.models import Route


class SurveySerializer(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(slug_field='username', source='car.user', read_only=True)
    driver = serializers.SlugRelatedField(slug_field='username', source='driver.user', read_only=True)
    route = serializers.SlugRelatedField(slug_field='name', read_only=True)
    car_name = serializers.CharField(max_length=100, write_only=True)
    driver_name = serializers.CharField(max_length=100, write_only=True)
    route_name = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Survey
        fields = '__all__'

    def create(self, validated_data):
        try:
            driver: Driver = Driver.objects.get(user__username=validated_data.pop('driver_name'))
        except Driver.DoesNotExist:
            raise NotFound('Driver does not exist!')

        try:
            car: Car = Car.objects.get(user__username=validated_data.pop('car_name'))
        except Car.DoesNotExist:
            raise NotFound('Car does not exist!')

        try:
            route: Route = Route.objects.get(name=validated_data.pop('route_name'))
        except Route.DoesNotExist:
            raise NotFound('Route does not exist!')

        survey: Survey = Survey(driver=driver, car=car, route=route, **validated_data)
        survey.save()
        return survey

