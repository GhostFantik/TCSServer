from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound
from Repairs.models import RepairRequest, Repair, Tag, TypeRepair
from Auth.models import Driver, Mechanic, Admin, Car


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TypeRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeRepair
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

    mechanic_first_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                                source="mechanic.user.first_name")
    mechanic_last_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                               source="mechanic.user.last_name")
    mechanic_third_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                                source="mechanic.user.third_name")

    admin_first_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                             source="request.admin.user.first_name")
    admin_last_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                            source="request.admin.user.last_name")
    admin_third_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                             source="request.admin.user.third_name")

    car_name = serializers.CharField(max_length=100, write_only=True)
    driver_name = serializers.CharField(max_length=100, write_only=True, required=False, allow_blank=True)
    admin_name = serializers.CharField(max_length=100, write_only=True, required=False, allow_blank=True)
    mechanic_name = serializers.CharField(max_length=100, write_only=True, required=False, allow_blank=True)
    tag_list = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True)

    class Meta:
        model = RepairRequest
        fields = '__all__'

    def create(self, validated_data):
        if len({'admin_name', 'mechanic_name', 'driver_name'} & set(validated_data.keys())) != 1:
            raise ParseError('admin_name or mechanic_name or driver_name must be')
        try:
            car: Car = Car.objects.get(user__username=validated_data.pop('car_name'))
        except Car.DoesNotExist:
            raise NotFound('Car does not exist!')
        try:
            tag_list = validated_data.pop('tag_list')
            tags = Tag.objects.filter(name__in=tag_list)
            if len(tag_list) != len(tags):
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


class RepairSerializer(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(slug_field='username', source='car.user', read_only=True)
    admin = serializers.SlugRelatedField(slug_field='username', source='admin.user', read_only=True,
                                         allow_empty=True)
    mechanic = serializers.SlugRelatedField(slug_field='username', source='mechanic.user', read_only=True,
                                            allow_empty=True)
    request = serializers.PrimaryKeyRelatedField(read_only=True, allow_empty=True, allow_null=True)
    tags = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    types_repair = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    description = serializers.CharField(max_length=500, read_only=True, source="request.info", allow_null=True)

    mechanic_first_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                                source="mechanic.user.first_name")
    mechanic_last_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                               source="mechanic.user.last_name")
    mechanic_third_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                                source="mechanic.user.third_name")

    mechanic_request_first_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                                        source="request.mechanic.user.first_name")
    mechanic_request_last_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                                       source="request.mechanic.user.last_name")
    mechanic_request_third_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                                        source="request.mechanic.user.third_name")

    driver_first_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                              source="request.driver.user.first_name")
    driver_last_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                             source="request.driver.user.last_name")
    driver_third_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                              source="request.driver.user.third_name")

    admin_first_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                             source="admin.user.first_name")
    admin_last_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                            source="admin.user.last_name")
    admin_third_name = serializers.CharField(max_length=100, read_only=True, allow_null=True,
                                             source="admin.user.third_name")

    car_name = serializers.CharField(max_length=100, write_only=True)
    admin_name = serializers.CharField(max_length=100, write_only=True, required=False, allow_blank=True)
    mechanic_name = serializers.CharField(max_length=100, write_only=True, required=False, allow_blank=True)
    request_pk = serializers.IntegerField(min_value=0, write_only=True, required=False)
    tag_list = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True)
    types_list = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True)

    class Meta:
        model = Repair
        fields = '__all__'

    def create(self, validated_data):
        if len({'admin_name', 'mechanic_name'} & set(validated_data.keys())) != 1:
            raise ParseError('admin_name or mechanic_name must be')
        try:
            car = Car.objects.get(user__username=validated_data.pop('car_name'))
        except Car.DoesNotExist:
            raise NotFound('Car does not exist!')
        try:
            tag_list = validated_data.pop('tag_list')
            tags = Tag.objects.filter(name__in=tag_list)
            if len(tag_list) != len(tags):
                raise Tag.DoesNotExist
        except Tag.DoesNotExist:
            raise NotFound('Tag does not exist!')
        try:
            types_list = validated_data.pop('types_list')
            types_repair = TypeRepair.objects.filter(name__in=types_list)
            if len(types_list) != len(types_repair):
                raise TypeRepair.DoesNotExist
        except TypeRepair.DoesNotExist:
            raise NotFound('TypeRepair does not exist!')

        request = None
        if 'request_pk' in validated_data:
            try:
                request = RepairRequest.objects.get(pk=validated_data.pop('request_pk'))
                request.completed = True
                request.save()
            except RepairRequest.DoesNotExist:
                raise NotFound('RepairRequest does not exist!')
        try:
            if 'mechanic_name' in validated_data:
                mechanic: Mechanic = Mechanic.objects.get(user__username=validated_data.pop('mechanic_name'))
                repair: Repair = Repair(car=car, mechanic=mechanic, **validated_data)
            elif 'admin_name' in validated_data:
                admin: Admin = Admin.objects.get(user__username=validated_data.pop('admin_name'))
                repair: Repair = Repair(car=car, admin=admin, **validated_data)
            else:
                raise ParseError('Bad request!')
        except Mechanic.DoesNotExist:
            raise NotFound('Mechanic does not exist!')
        except Admin.DoesNotExist:
            raise NotFound('Admin does not exist!')

        repair.request = request
        repair.save()
        repair.tags.add(*list(tags))
        repair.types_repair.add(*list(types_repair))
        return repair
