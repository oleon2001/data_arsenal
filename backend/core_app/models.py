# core_app/models.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField # Para Array de NUMERIC
from django.utils import timezone

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
        # Asegúrate de que User.UserType.ADMIN esté definido antes de llamar a esto
        # o pasa un valor de string directamente si es necesario durante la inicialización.
        extra_fields.setdefault('type', 'admin') # Usando el valor string directamente

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# --- Modelos ---

class ServicePlan(models.Model):
    # Mapea a service_plans
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_name = models.TextField() # TEXT en SQL
    cost = models.DecimalField(max_digits=10, decimal_places=2) # NUMERIC(10,2)
    max_vehicles = models.IntegerField()
    registered_vehicles = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True) # TEXT, puede ser nulo
    created_at = models.DateTimeField(default=timezone.now) # TIMESTAMPTZ NOT NULL DEFAULT now()
    updated_at = models.DateTimeField(default=timezone.now) # TIMESTAMPTZ NOT NULL DEFAULT now()

    def __str__(self):
        return self.plan_name

    class Meta:
        verbose_name = "Plan de Servicio"
        verbose_name_plural = "Planes de Servicio"
        db_table = 'service_plans' # Para coincidir con tu nombre de tabla SQL

class Company(models.Model):
    # Mapea a companies
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.TextField()
    rfc = models.TextField(blank=True, null=True)
    manager_name = models.TextField(blank=True, null=True)
    manager_email = models.EmailField(blank=True, null=True) # Usar EmailField para validación
    country = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True) # CHAR(3)
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
    # Mapea a users
    # Para el tipo ENUM 'user_type'
    class UserType(models.TextChoices):
        OWNER = 'owner', 'Propietario'
        ADMIN = 'admin', 'Administrador'
        STANDARD = 'standard', 'Estándar'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True) # TEXT NOT NULL UNIQUE
    # La contraseña es manejada por AbstractBaseUser
    type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.STANDARD) # user_type
    name = models.TextField()
    last_name = models.TextField()
    phone = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    company_info = models.JSONField(blank=True, null=True) # JSONB
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    renewal_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True) # Requerido por AbstractBaseUser
    is_staff = models.BooleanField(default=False) # Requerido para el admin de Django

    objects = UserManager()

    USERNAME_FIELD = 'email' # Usar email para login
    REQUIRED_FIELDS = ['name', 'last_name', 'type'] # Campos requeridos al crear superusuario

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = 'users'

class InvitationCode(models.Model):
    # Mapea a invitation_codes
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE) # NOT NULL
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
    # Mapea a receptors
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # MACADDR no es un tipo nativo de Django. Usamos CharField.
    # Podrías añadir un validador personalizado si es necesario.
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
    # Mapea a sensors
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
    # Mapea a vehicles
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True) # Podría ser un CharField con choices si hay tipos fijos
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
    # Mapea a sensor_assignments
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE) # NOT NULL
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) # NOT NULL
    position = models.TextField(blank=True, null=True)
    assigned_at = models.DateTimeField(default=timezone.now)
    unassigned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Sensor {self.sensor_id} a Vehículo {self.vehicle_id}"

    class Meta:
        verbose_name = "Asignación de Sensor"
        verbose_name_plural = "Asignaciones de Sensores"
        db_table = 'sensor_assignments'
        unique_together = [['sensor', 'vehicle', 'unassigned_at']] # Corregido: usar nombres de campo

class SensorReading(models.Model):
    # Mapea a sensor_readings
    id = models.BigAutoField(primary_key=True) # BIGSERIAL
    receptor = models.ForeignKey(Receptor, on_delete=models.SET_NULL, null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    unique_id = models.UUIDField(null=True, blank=True) # UUID, puede ser nulo
    avg = ArrayField(models.DecimalField(max_digits=10, decimal_places=2), blank=True, null=True) # NUMERIC[]
    peak = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # NUMERIC
    qos = models.IntegerField(blank=True, null=True)
    rpsi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # NUMERIC
    rtemp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # NUMERIC
    rvolts = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # NUMERIC
    packet_timestamp = models.DateTimeField(blank=True, null=True) # TIMESTAMPTZ
    topic = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    raw_data = models.JSONField(blank=True, null=True) # JSONB
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

# --- Constantes para los prefijos de ID de receptor para las fórmulas de presión ---
PREFIJO_PRESION_1 = "RPS_A"  # Ejemplo para la fórmula 2.8 * psi + 87.20
PREFIJO_PRESION_2 = "RPS_B"  # Ejemplo para la fórmula 1.572 * psi + 98.428
PREFIJO_PRESION_3 = "RPS_C"  # Ejemplo para la fórmula 0.688 * psi + 99.312
# Puedes añadir más prefijos si tienes más fórmulas de presión

class Device(models.Model):
    device_id = models.CharField(
        max_length=100,
        unique=True,
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.device_id})"

    class Meta:
        ordering = ['name']
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        # db_table = 'devices' # Opcional, Django generará core_app_device por defecto

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
    ]
    data_type = models.CharField(
        max_length=50,
        choices=DATA_TYPE_CHOICES,
        help_text="Tipo de dato medido"
    )
    data_value = models.FloatField(help_text="Valor numérico del dato medido")
    unit = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Unidad de medida (ej: °C, %, hPa)"
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora de la medición"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.get_data_type_display()}: {self.data_value} {self.unit or ''} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def get_unit_display(self):
        if self.unit:
            return self.unit
        default_units = {
            'temperature': '°C',
            'humidity': '%',
            'pressure': 'hPa',
            'light_intensity': 'lux',
            'co2': 'ppm',
            'voltage': 'V',
            'current': 'A',
            'power': 'W',
            'water_level': 'cm',
        }
        return default_units.get(self.data_type, '')

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Dato de Dispositivo"
        verbose_name_plural = "Datos de Dispositivos"
        # db_table = 'device_data' # Opcional
        indexes = [
            models.Index(fields=['device', 'data_type', '-timestamp']),
        ]
