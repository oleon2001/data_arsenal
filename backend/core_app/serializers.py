# core_app/serializers.py
from rest_framework import serializers
from .models import (
    ServicePlan, Company, User, InvitationCode,
    Receptor, Sensor, Vehicle, SensorAssignment, SensorReading,
    Device, DeviceData  # Cambiado Data a DeviceData si ese es el nombre correcto del modelo
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
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'id', 'email', 'type', 'name', 'last_name', 'phone', 'birthday',
            'language', 'company', 'company_info', 'created_at', 'updated_at',
            'deleted', 'renewal_date', 'is_active', 'is_staff', 'password'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
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

class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Device.
    """
    class Meta:
        model = Device
        fields = '__all__'


# Renombrado de DataSerializer a DeviceDataSerializer
class DeviceDataSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo DeviceData (anteriormente Data).
    Incluye campos calculados para presión, temperatura y voltaje convertidos.
    """
    presion_kpa = serializers.SerializerMethodField(help_text="Presión calculada en kilopascales (kPa).")
    temperatura_celsius = serializers.SerializerMethodField(help_text="Temperatura calculada en grados Celsius (°C).")
    voltaje_volts = serializers.SerializerMethodField(help_text="Voltaje calculado en Volts (V).")
    # device_name = serializers.CharField(source='device.name', read_only=True) # Ejemplo si quieres el nombre

    class Meta:
        model = DeviceData # Asegúrate que el modelo se llama DeviceData
        fields = [
            'id',
            'device',
            # 'device_name',
            'timestamp',
            'data_type', # Asumiendo que este campo existe en DeviceData
            'data_value', # Asumiendo que este campo existe en DeviceData
            'unit', # Asumiendo que este campo existe en DeviceData
            'prefijo_id_rt',
            'valor_crudo_psi',
            'valor_crudo_temp',
            'valor_crudo_volt',
            'presion_kpa',
            'temperatura_celsius',
            'voltaje_volts',
            'latitude',
            'longitude',
            'altitude',
            'speed',
            'course',
            'satellites'
        ]
        read_only_fields = [
            'timestamp',
            'presion_kpa',
            'temperatura_celsius',
            'voltaje_volts',
        ]

    def get_presion_kpa(self, obj: DeviceData) -> float | None:
        """
        Obtiene el valor de presión calculado desde el método del modelo.
        """
        # Asegúrate que el objeto obj (instancia de DeviceData) tenga este método
        if hasattr(obj, 'get_presion_kpa'):
            return obj.get_presion_kpa()
        return None

    def get_temperatura_celsius(self, obj: DeviceData) -> float | None:
        """
        Obtiene el valor de temperatura calculado desde el método del modelo.
        """
        if hasattr(obj, 'get_temperatura_celsius'):
            return obj.get_temperatura_celsius()
        return None

    def get_voltaje_volts(self, obj: DeviceData) -> float | None:
        """
        Obtiene el valor de voltaje calculado desde el método del modelo.
        """
        if hasattr(obj, 'get_voltaje_volts'):
            return obj.get_voltaje_volts()
        return None

# Nuevo serializador para la creación de DeviceData
class DeviceDataCreateSerializer(serializers.ModelSerializer):
    """
    Serializador para crear instancias de DeviceData.
    Podría tener campos diferentes o validaciones específicas para la creación.
    """
    class Meta:
        model = DeviceData # Asegúrate que el modelo se llama DeviceData
        fields = [ # Define los campos que se esperan en una solicitud POST
            'device',
            'data_type',
            'data_value',
            'unit',
            'prefijo_id_rt',
            'valor_crudo_psi',
            'valor_crudo_temp',
            'valor_crudo_volt',
            'latitude',
            'longitude',
            'altitude',
            'speed',
            'course',
            'satellites'
            # El timestamp usualmente se maneja automáticamente o se establece en la vista
        ]
        # Puedes añadir validaciones extra aquí si es necesario para la creación
