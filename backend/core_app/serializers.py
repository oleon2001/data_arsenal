from rest_framework import serializers
from .models import (
    ServicePlan, Company, User, InvitationCode,
    Receptor, Sensor, Vehicle, SensorAssignment, SensorReading,
    Device, Data
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



class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Device.
    """
    class Meta:
        model = Device
        fields = '__all__' # Incluye todos los campos del modelo Device.
        # O puedes especificar campos: fields = ['id', 'name', 'description']


class DataSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Data.
    Incluye campos calculados para presión, temperatura y voltaje convertidos.
    """
    # --- Campos calculados ---
    presion_kpa = serializers.SerializerMethodField(help_text="Presión calculada en kilopascales (kPa).")
    temperatura_celsius = serializers.SerializerMethodField(help_text="Temperatura calculada en grados Celsius (°C).")
    voltaje_volts = serializers.SerializerMethodField(help_text="Voltaje calculado en Volts (V).")

    # device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = Data
        fields = [
            'id', 
            'device',               # ID del dispositivo asociado
            # 'device_name',        # Descomentar para incluir el nombre del dispositivo
            'timestamp',
            'prefijo_id_rt',        # Prefijo para identificar la fórmula
            'valor_crudo_psi',      # Valor crudo para presión
            'valor_crudo_temp',     # Valor crudo para temperatura
            'valor_crudo_volt',     # Valor crudo para voltaje
            'presion_kpa',          # Valor de presión calculado/convertido
            'temperatura_celsius',  # Valor de temperatura calculado/convertido
            'voltaje_volts',        # Valor de voltaje calculado/convertido
            'latitude', 
            'longitude', 
            'altitude', 
            'speed', 
            'course', 
            'satellites'
        ]
        read_only_fields = [
            'timestamp', # El timestamp se genera automáticamente
            'presion_kpa',
            'temperatura_celsius',
            'voltaje_volts',
        ]

    def get_presion_kpa(self, obj: Data) -> float | None:
        """
        Obtiene el valor de presión calculado desde el método del modelo.
        """
        return obj.get_presion_kpa()

    def get_temperatura_celsius(self, obj: Data) -> float | None:
        """
        Obtiene el valor de temperatura calculado desde el método del modelo.
        """
        return obj.get_temperatura_celsius()

    def get_voltaje_volts(self, obj: Data) -> float | None:
        """
        Obtiene el valor de voltaje calculado desde el método del modelo.
        """
        return obj.get_voltaje_volts()

