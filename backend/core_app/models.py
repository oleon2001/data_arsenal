# core_app/models.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField # Para Array de NUMERIC
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ # Para los related_name
# from django.utils import timezone # Ya está importado arriba

# --- Gestor de Usuario Personalizado ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un Usuario con el email y contraseña dados.
        """
        if not email:
            raise ValueError('El Email debe ser establecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hashea la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el email y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('type', User.UserType.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# --- Modelos ---

class ServicePlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_name = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    max_vehicles = models.IntegerField()
    registered_vehicles = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.plan_name

    class Meta:
        verbose_name = "Plan de Servicio"
        verbose_name_plural = "Planes de Servicio"
        db_table = 'service_plans'

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.TextField()
    rfc = models.TextField(blank=True, null=True)
    manager_name = models.TextField(blank=True, null=True)
    manager_email = models.EmailField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.SET_NULL, null=True, blank=True)
    last_payment_date = models.DateField(blank=True, null=True)
    next_payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Compañía"
        verbose_name_plural = "Compañías"
        db_table = 'companies'

class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        OWNER = 'owner', 'Propietario'
        ADMIN = 'admin', 'Administrador'
        STANDARD = 'standard', 'Estándar'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.STANDARD)
    name = models.TextField()
    last_name = models.TextField()
    phone = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    company_info = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    renewal_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="core_app_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="core_app_user_permissions_set",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name', 'type']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = 'users'

class InvitationCode(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(blank=True, null=True)
    used_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invitations_used')
    used_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = "Código de Invitación"
        verbose_name_plural = "Códigos de Invitación"
        db_table = 'invitation_codes'

class Receptor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mac_address = models.CharField(max_length=17, unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.mac_address

    class Meta:
        verbose_name = "Receptor"
        verbose_name_plural = "Receptores"
        db_table = 'receptors'

class Sensor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receptor = models.ForeignKey(Receptor, on_delete=models.CASCADE, null=True, blank=True)
    sensor_identifier = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sensor_identifier or str(self.id)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"
        db_table = 'sensors'

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.alias or str(self.id)

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        db_table = 'vehicles'

class SensorAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    position = models.TextField(blank=True, null=True)
    assigned_at = models.DateTimeField(default=timezone.now)
    unassigned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Sensor {self.sensor_id} a Vehículo {self.vehicle_id}"

    class Meta:
        verbose_name = "Asignación de Sensor"
        verbose_name_plural = "Asignaciones de Sensores"
        db_table = 'sensor_assignments'
        unique_together = [['sensor', 'vehicle', 'unassigned_at']]

class SensorReading(models.Model):
    id = models.BigAutoField(primary_key=True)
    receptor = models.ForeignKey(Receptor, on_delete=models.SET_NULL, null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    unique_id = models.UUIDField(null=True, blank=True)
    avg = ArrayField(models.DecimalField(max_digits=10, decimal_places=2), blank=True, null=True)
    peak = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qos = models.IntegerField(blank=True, null=True)
    rpsi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rtemp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rvolts = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    packet_timestamp = models.DateTimeField(blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    raw_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Lectura {self.id} - Sensor {self.sensor_id if self.sensor else 'N/A'}"

    class Meta:
        verbose_name = "Lectura de Sensor"
        verbose_name_plural = "Lecturas de Sensores"
        db_table = 'sensor_readings'
        indexes = [
            models.Index(fields=['receptor']),
            models.Index(fields=['sensor']),
            models.Index(fields=['created_at']),
        ]

PREFIJO_PRESION_1 = "RPS_A"
PREFIJO_PRESION_2 = "RPS_B"
PREFIJO_PRESION_3 = "RPS_C"

class Device(models.Model):
    device_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,    # TEMPORALMENTE: Permitir nulos para la primera migración
        blank=True,   # TEMPORALMENTE: Permitir blank para la primera migración
        # default=lambda: uuid.uuid4().hex, # Se quitará temporalmente el default funcional
        help_text="Identificador único del dispositivo, ej: ESP32_LivingRoom_Sensor1"
    )
    name = models.CharField(
        max_length=100,
        help_text="Nombre descriptivo del dispositivo"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ubicación del dispositivo"
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="Dirección IP actual del dispositivo (opcional)"
    )
    mac_address = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        help_text="Dirección MAC del dispositivo (opcional)"
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        help_text="Última vez que el dispositivo envió datos o se actualizó"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si el dispositivo está activo y se espera que envíe datos"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.device_id or 'ID no asignado'})" # Manejar None temporalmente

    class Meta:
        ordering = ['name']
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        # db_table = 'devices' # Descomenta y ajusta si tienes un nombre de tabla personalizado

class Data(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='data_records',
        help_text="Dispositivo asociado a este dato",
        null=True,  # <-- Asegúrate de que esto esté presente
        blank=True  # <-- Opcional, para admin/forms
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora de la medición"
    )
    prefijo_id_rt = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Prefijo para identificar la fórmula de cálculo, ej: RPS_A"
    )
    valor_crudo_psi = models.FloatField(
        blank=True,
        null=True,
        help_text="Valor crudo de presión (ej: del sensor en PSI)"
    )
    valor_crudo_temp = models.FloatField(
        blank=True,
        null=True,
        help_text="Valor crudo de temperatura (ej: del sensor)"
    )
    valor_crudo_volt = models.FloatField(
        blank=True,
        null=True,
        help_text="Valor crudo de voltaje (ej: del sensor)"
    )
    latitude = models.FloatField(blank=True, null=True, help_text="Latitud geográfica")
    longitude = models.FloatField(blank=True, null=True, help_text="Longitud geográfica")
    altitude = models.FloatField(blank=True, null=True, help_text="Altitud en metros")
    speed = models.FloatField(blank=True, null=True, help_text="Velocidad en m/s o km/h según convención")
    course = models.FloatField(blank=True, null=True, help_text="Dirección del movimiento en grados")
    satellites = models.IntegerField(blank=True, null=True, help_text="Número de satélites GPS")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_presion_kpa(self) -> float | None:
        if self.valor_crudo_psi is None or self.prefijo_id_rt is None:
            return None
        psi = self.valor_crudo_psi
        if self.prefijo_id_rt == PREFIJO_PRESION_1:
            return (2.8 * psi) + 87.20
        elif self.prefijo_id_rt == PREFIJO_PRESION_2:
            return (1.572 * psi) + 98.428
        elif self.prefijo_id_rt == PREFIJO_PRESION_3:
            return (0.688 * psi) + 99.312
        return None

    def get_temperatura_celsius(self) -> float | None:
        if self.valor_crudo_temp is None:
            return None
        return self.valor_crudo_temp

    def get_voltaje_volts(self) -> float | None:
        if self.valor_crudo_volt is None:
            return None
        return self.valor_crudo_volt

    def __str__(self):
        device_identifier = self.device.device_id if self.device and self.device.device_id else "Dispositivo Desconocido"
        return f"Data for {device_identifier} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Dato de Telemetría (Antiguo)"
        verbose_name_plural = "Datos de Telemetría (Antiguos)"
        db_table = 'telemetry_data'
        ordering = ['-timestamp', 'device']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['prefijo_id_rt']),
        ]

class DeviceData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, related_name='data_points', on_delete=models.CASCADE)

    DATA_TYPE_CHOICES = [
        ('temperature', 'Temperatura'),
        ('humidity', 'Humedad'),
        ('pressure', 'Presión Atmosférica'),
        ('light_intensity', 'Intensidad de Luz'),
        ('co2', 'Nivel de CO2'),
        ('voltage', 'Voltaje'),
        ('current', 'Corriente'),
        ('power', 'Potencia'),
        ('motion', 'Movimiento Detectado'),
        ('door_status', 'Estado de Puerta'),
        ('water_level', 'Nivel de Agua'),
        ('generic', 'Dato Genérico'),
        ('raw_psi', 'Presión Cruda PSI'),
        ('raw_temp', 'Temperatura Cruda'),
        ('raw_volt', 'Voltaje Crudo'),
    ]
    data_type = models.CharField(
        max_length=50,
        choices=DATA_TYPE_CHOICES,
        help_text="Tipo de dato medido"
    )
    data_value = models.FloatField(help_text="Valor numérico del dato medido (procesado/convertido)")
    
    unit = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Unidad de medida (ej: °C, %, hPa, kPa, V)"
    )
    prefijo_id_rt = models.CharField(max_length=50, blank=True, null=True)
    valor_crudo_psi = models.FloatField(blank=True, null=True)
    valor_crudo_temp = models.FloatField(blank=True, null=True)
    valor_crudo_volt = models.FloatField(blank=True, null=True)
    
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    course = models.FloatField(blank=True, null=True)
    satellites = models.IntegerField(blank=True, null=True)

    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora de la medición"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.device.name} - {self.get_data_type_display()}: {self.data_value} {self.unit or ''} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def get_unit_display(self):
        if self.unit:
            return self.unit
        default_units = {
            'temperature': '°C',
            'humidity': '%',
            'pressure': 'kPa',
            'light_intensity': 'lux',
            'co2': 'ppm',
            'voltage': 'V',
            'current': 'A',
            'power': 'W',
            'water_level': 'cm',
            'raw_psi': 'PSI',
            'raw_temp': 'RAW',
            'raw_volt': 'RAW',
        }
        return default_units.get(self.data_type, '')
        
    def get_presion_kpa_from_device_data(self) -> float | None:
        if self.data_type == 'pressure' and self.unit == 'kPa':
             return self.data_value
        if self.data_type == 'raw_psi' and self.valor_crudo_psi is not None and self.prefijo_id_rt:
            psi = self.valor_crudo_psi
            if self.prefijo_id_rt == PREFIJO_PRESION_1: return (2.8 * psi) + 87.20
            elif self.prefijo_id_rt == PREFIJO_PRESION_2: return (1.572 * psi) + 98.428
            elif self.prefijo_id_rt == PREFIJO_PRESION_3: return (0.688 * psi) + 99.312
        return None

    def get_temperatura_celsius_from_device_data(self) -> float | None:
        if self.data_type == 'temperature' and self.unit == '°C':
            return self.data_value
        if self.data_type == 'raw_temp' and self.valor_crudo_temp is not None:
            return self.valor_crudo_temp
        return None

    def get_voltaje_volts_from_device_data(self) -> float | None:
        if self.data_type == 'voltage' and self.unit == 'V':
            return self.data_value
        if self.data_type == 'raw_volt' and self.valor_crudo_volt is not None:
            return self.valor_crudo_volt
        return None

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Dato de Dispositivo"
        verbose_name_plural = "Datos de Dispositivos"
        # db_table = 'device_data' # Descomenta y ajusta si tienes un nombre de tabla personalizado
        indexes = [
            models.Index(fields=['device', 'data_type', '-timestamp']),
        ]
