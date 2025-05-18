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
        extra_fields.setdefault('type', User.UserType.ADMIN) # O OWNER si prefieres

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# --- Modelos ---

class ServicePlan(models.Model):
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
    # Para el tipo ENUM 'user_type'
    class UserType(models.TextChoices):
        OWNER = 'owner', 'Propietario'
        ADMIN = 'admin', 'Administrador'
        STANDARD = 'standard', 'Estándar'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True) # TEXT NOT NULL UNIQUE
    # La contraseña es manejada por AbstractBaseUser
    type = models.CharField(max_length=10, choices=UserType.choices) # user_type
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
        unique_together = [['sensor_id', 'vehicle_id', 'unassigned_at']] # Para evitar múltiples asignaciones activas

class SensorReading(models.Model):
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
        return f"Lectura {self.id} - Sensor {self.sensor_id}"

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
    """
    Modelo para representar un dispositivo.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre del Dispositivo")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

class Data(models.Model):
    """
    Modelo para almacenar los datos recibidos de los dispositivos,
    incluyendo valores crudos y métodos para obtener valores procesados.
    """
    device = models.ForeignKey(
        Device, 
        on_delete=models.CASCADE, 
        related_name='data_points', 
        null=True, 
        blank=True,
        verbose_name="Dispositivo Asociado"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Marca de Tiempo")
    
    prefijo_id_rt = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        help_text="Prefijo identificador del receptor/sensor para seleccionar la fórmula de conversión.",
        verbose_name="Prefijo ID Receptor"
    )

    # --- Valores crudos de los sensores ---
    valor_crudo_psi = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Valor crudo de presión en PSI (libras por pulgada cuadrada).",
        verbose_name="Valor Crudo Presión (PSI)"
    )
    valor_crudo_temp = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Valor crudo de temperatura (unidad original del sensor).",
        verbose_name="Valor Crudo Temperatura"
    )
    valor_crudo_volt = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Valor crudo de voltaje.",
        verbose_name="Valor Crudo Voltaje"
    )

    # --- Otros campos que ya existían ---
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitud")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitud")
    altitude = models.FloatField(null=True, blank=True, verbose_name="Altitud")
    speed = models.FloatField(null=True, blank=True, verbose_name="Velocidad")
    course = models.FloatField(null=True, blank=True, verbose_name="Curso")
    satellites = models.IntegerField(null=True, blank=True, verbose_name="Satélites")
    
    def __str__(self):
        device_name = self.device.name if self.device else "Dispositivo Desconocido"
        return f"Datos de {device_name} en {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_presion_kpa(self):
        """
        Calcula la presión en kPa basándose en el valor crudo PSI y el prefijo_id_rt.
        Retorna el valor calculado o None si no se puede calcular.
        """
        if self.valor_crudo_psi is None:
            return None

        rpsi = float(self.valor_crudo_psi)

        if self.prefijo_id_rt == PREFIJO_PRESION_1:
            return (2.8 * rpsi) + 87.20
        elif self.prefijo_id_rt == PREFIJO_PRESION_2:
            return (1.572 * rpsi) + 98.428
        elif self.prefijo_id_rt == PREFIJO_PRESION_3:
            return (0.688 * rpsi) + 99.312
        else:
            return None

    def get_temperatura_celsius(self):
        """
        Calcula la temperatura en °C.
        Fórmula: {rtemp} - 55
        Retorna el valor calculado o None si el valor crudo no está disponible.
        """
        if self.valor_crudo_temp is None:
            return None
        rtemp = float(self.valor_crudo_temp)
        return rtemp - 55

    def get_voltaje_volts(self):
        """
        Calcula el voltaje en V.
        Fórmula: 0.01 * {rvolts} + 1.22
        Retorna el valor calculado o None si el valor crudo no está disponible.
        """
        if self.valor_crudo_volt is None:
            return None
        rvolts = float(self.valor_crudo_volt)
        return (0.01 * rvolts) + 1.22

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Dato"
        verbose_name_plural = "Datos"
