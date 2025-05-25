# core_app/serializers.py
from rest_framework import serializers
from .models import (
    ServicePlan, Company, User, InvitationCode,
    Receptor, Sensor, Vehicle, SensorAssignment, SensorReading,
    Device, DeviceData
    # Los siguientes modelos no están en models.py y se comentan sus serializadores abajo:
    # Planta, Area, Linea, Equipo, PuntoMonitoreo,
    # Variable, UnidadMedida, ValorVariable, Limite, Alerta, Reporte,
    # Notificacion, Rol, Permiso
)

class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer): # Nombre cambiado de EmpresaSerializer
    class Meta:
        model = Company # Modelo cambiado a Company
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password", style={'input_type': 'password'})
    type = serializers.ChoiceField(choices=User.UserType.choices, required=False) # Hacerlo opcional y default en el modelo o vista

    class Meta:
        model = User
        fields = ['email', 'name', 'last_name', 'password', 'password2', 'type', 'phone', 'birthday', 'language', 'company']
        extra_kwargs = {
            'name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        # El email ya es validado como unique por el modelo User.
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user_type = validated_data.pop('type', User.UserType.STANDARD) # Default si no se provee
        
        # Asegurar que 'company' sea una instancia o None, no un UUID string si viene de un form no validado.
        # Esto usualmente lo maneja DRF si el campo es un PrimaryKeyRelatedField, pero es bueno estar atento.
        
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            type=user_type,
            phone=validated_data.get('phone'),
            birthday=validated_data.get('birthday'),
            language=validated_data.get('language'),
            company=validated_data.get('company') # Puede ser None
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, style={'input_type': 'password'})
    company_name = serializers.CharField(source='company.company_name', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'type', 'name', 'last_name', 'phone', 'birthday',
            'language', 'company', 'company_name', 'company_info', 'created_at', 'updated_at',
            'deleted', 'renewal_date', 'is_active', 'is_staff', 'password',
            'groups', 'user_permissions' # Incluir para gestión de permisos si es necesario
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff', 'company_name']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email") # Cambiado de username a email
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email') # Cambiado de username a email
        password = attrs.get('password')

        if email and password:
            # El authenticate se hace en la vista
            pass
        else:
            msg = 'Debe incluir "email" y "password".' # Cambiado de username a email
            raise serializers.ValidationError(msg, code='authorization')
        return attrs


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
    class Meta:
        model = Device
        fields = '__all__'

class DeviceDataSerializer(serializers.ModelSerializer):
    presion_kpa = serializers.SerializerMethodField(read_only=True)
    temperatura_celsius = serializers.SerializerMethodField(read_only=True)
    voltaje_volts = serializers.SerializerMethodField(read_only=True)
    device_id_str = serializers.CharField(source='device.device_id', read_only=True, allow_null=True)


    class Meta:
        model = DeviceData
        fields = [
            'id', 'device', 'device_id_str', 'timestamp', 'data_type', 'data_value', 'unit',
            'prefijo_id_rt', 'valor_crudo_psi', 'valor_crudo_temp', 'valor_crudo_volt',
            'presion_kpa', 'temperatura_celsius', 'voltaje_volts',
            'latitude', 'longitude', 'altitude', 'speed', 'course', 'satellites',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'presion_kpa', 'temperatura_celsius', 'voltaje_volts', 'device_id_str']

    def get_presion_kpa(self, obj):
        return obj.get_presion_kpa_from_device_data()

    def get_temperatura_celsius(self, obj):
        return obj.get_temperatura_celsius_from_device_data()

    def get_voltaje_volts(self, obj):
        return obj.get_voltaje_volts_from_device_data()

class DeviceDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = [
            'device', 'data_type', 'data_value', 'unit', 'prefijo_id_rt',
            'valor_crudo_psi', 'valor_crudo_temp', 'valor_crudo_volt',
            'latitude', 'longitude', 'altitude', 'speed', 'course', 'satellites',
            'timestamp' # Permitir que el timestamp sea enviado o usar default
        ]
        extra_kwargs = {
            'timestamp': {'required': False} # Hacer el timestamp opcional en la creación
        }


# --- Serializadores Comentados (Dependen de Modelos No Encontrados) ---
# class PlantaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Planta
#         fields = '__all__'

# class AreaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Area
#         fields = '__all__'

# class LineaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Linea
#         fields = '__all__'

# class EquipoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Equipo
#         fields = '__all__'

# class PuntoMonitoreoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PuntoMonitoreo
#         fields = '__all__'

# class VariableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Variable
#         fields = '__all__'

# class UnidadMedidaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UnidadMedida
#         fields = '__all__'

# class ValorVariableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ValorVariable
#         fields = '__all__'

# class LimiteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Limite
#         fields = '__all__'

# class AlertaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Alerta
#         fields = '__all__'

# class ReporteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reporte
#         fields = '__all__'

# class NotificacionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notificacion
#         fields = '__all__'

# class RolSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rol
#         fields = '__all__'

# class PermisoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permiso
#         fields = '__all__'
