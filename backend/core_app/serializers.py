from rest_framework import serializers
from .models import (
    ServicePlan, Company, User, InvitationCode,
    Receptor, Sensor, Vehicle, SensorAssignment, SensorReading
)

class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # Para asegurar que la contraseña no se devuelva en las respuestas GET
    # y para manejar la creación/actualización de contraseñas correctamente.
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        # Excluye campos sensibles o innecesarios en la API pública
        fields = [
            'id', 'email', 'type', 'name', 'last_name', 'phone', 'birthday',
            'language', 'company', 'company_info', 'created_at', 'updated_at',
            'deleted', 'renewal_date', 'is_active', 'is_staff', 'password'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff']

    def create(self, validated_data):
        # Llama al método create_user del manager para hashear la contraseña
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Maneja la actualización de la contraseña si se proporciona
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class InvitationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = '__all__'

class ReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptor
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class SensorAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorAssignment
        fields = '__all__'

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'

