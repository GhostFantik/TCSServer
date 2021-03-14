from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound
from Repairs.models import RepairRequest, Repair, Tag, TypeRepair
from Auth.models import Driver, Mechanic, Admin, Car


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RepairRequestSerializer(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(slug_field='username', source='car.user', read_only=True)
    driver = serializers.SlugRelatedField(slug_field='username', source='driver.user', read_only=True,
                                          allow_empty=True)
    admin = serializers.SlugRelatedField(slug_field='username', source="admin.user", read_only=True,
                                         allow_empty=True)
    mechanic = serializers.SlugRelatedField(slug_field='username', source='mechanic.user', read_only=True,
                                            allow_empty=True)
    tags = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    completed = serializers.BooleanField(read_only=True)

    car_name = serializers.CharField(max_length=100, write_only=True)
    driver_name = serializers.CharField(max_length=100, write_only=True, required=False)
    admin_name = serializers.CharField(max_length=100, write_only=True, required=False)
    mechanic_name = serializers.CharField(max_length=100, write_only=True, required=False)
    tag_list = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True)

    class Meta:
        model = RepairRequest
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        if {'driver_name', 'admin_name', 'mechanic_name'}.isdisjoint(validated_data.keys()):
            raise ParseError('driver_name or admin_name or mechanic_name must be')
        try:
            car: Car = Car.objects.get(user__username=validated_data.pop('car_name'))
        except Car.DoesNotExist:
            raise NotFound('Car does not exist!')
        try:
            tag_list = validated_data.pop('tag_list')
            tags = Tag.objects.filter(name__in=tag_list)
            print(tag_list)
            print(tags.count())
            if len(tag_list) != tags.count():
                raise Tag.DoesNotExist
        except Tag.DoesNotExist:
            raise NotFound('Tag does not exist!')
        if 'driver_name' in validated_data:
            try:
                driver: Driver = Driver.objects.get(user__username=validated_data.pop('driver_name'))
            except Driver.DoesNotExist:
                raise NotFound('Driver does not exist!')
            repair_request: RepairRequest = RepairRequest(driver=driver, car=car, **validated_data)
        elif 'mechanic_name' in validated_data:
            try:
                mechanic: Mechanic = Mechanic.objects.get(user__username=validated_data.pop('mechanic_name'))
            except Mechanic.DoesNotExist:
                raise NotFound('Mechanic does not exist!')
            repair_request: RepairRequest = RepairRequest(mechanic=mechanic, car=car, **validated_data)
        elif 'admin_name' in validated_data:
            try:
                admin: Admin = Admin.objects.get(user__username=validated_data.pop('admin_name'))
            except Admin.DoesNotExist:
                raise NotFound('Admin does not exist!')
            repair_request: RepairRequest = RepairRequest(admin=admin, car=car, **validated_data)
        else:
            raise ParseError('Bad request!')
        repair_request.save()
        repair_request.tags.add(*list(tags))
        return repair_request
