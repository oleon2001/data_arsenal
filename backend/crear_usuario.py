import os
import django

# Configura el entorno de Django
# Asegúrate de que 'app.settings' sea la ruta correcta a tu archivo de configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Importa el modelo de usuario correcto desde core_app.models
from core_app.models import User

# --- Definición de los datos del usuario ---
email = "oswaldoleon72@example.com"
password = "prueba"
name = "oswaldo"  
last_name = "leon"
user_type = "admin"  # El campo 'type' es personalizado para tu modelo

# --- Lógica para crear el superusuario ---
if not User.objects.filter(email=email).exists():
    try:
        # Crea un superusuario. Este método se encarga de:
        # - Establecer la contraseña de forma segura (hasheada).
        # - Establecer is_staff=True.
        # - Establecer is_superuser=True.
        # - Establecer is_active=True (por defecto en tu manager).
        # Los campos name y last_name son parte de REQUIRED_FIELDS.
        # El campo 'type' se pasa como un campo extra.
        user = User.objects.create_superuser(
            email=email,
            password=password,
            name=name,
            last_name=last_name,
            type=user_type  # Pasando el campo personalizado 'type'
        )
        print(f"Superusuario '{email}' creado correctamente.")
        print(f"  - Email: {user.email}")
        print(f"  - Nombre: {user.name} {user.last_name}")
        print(f"  - Tipo (personalizado): {user.type}")
        print(f"  - ¿Es Staff?: {user.is_staff}")
        print(f"  - ¿Es Superusuario?: {user.is_superuser}")
        print(f"  - ¿Está Activo?: {user.is_active}")

    except Exception as e:
        print(f"Error al crear el superusuario: {e}")
else:
    try:
        existing_user = User.objects.get(email=email)
        print(f"El usuario '{email}' ya existe.")
        print(f"  - Email: {existing_user.email}")
        print(f"  - Nombre: {existing_user.name} {existing_user.last_name}")
        print(f"  - Tipo (personalizado): {existing_user.type}")
        print(f"  - ¿Es Staff?: {existing_user.is_staff}")
        print(f"  - ¿Es Superusuario?: {existing_user.is_superuser}")
        print(f"  - ¿Está Activo?: {existing_user.is_active}")
        # Si necesitas asegurarte de que sea superusuario y esté activo:
        if not existing_user.is_staff or not existing_user.is_superuser:
            existing_user.is_staff = True
            existing_user.is_superuser = True
            existing_user.set_password(password) # Re-establecer contraseña por si acaso
            existing_user.save()
            print(f"El usuario '{email}' existente ha sido actualizado a superusuario.")
        elif not existing_user.check_password(password):
            existing_user.set_password(password)
            existing_user.save()
            print(f"La contraseña del usuario '{email}' ha sido actualizada.")

    except User.DoesNotExist:
        # Esto no debería ocurrir si el filter().exists() fue True, pero es una buena práctica.
        print(f"Error: El usuario '{email}' se reportó como existente pero no se pudo recuperar.")
    except Exception as e:
        print(f"Error al verificar el usuario existente: {e}")

