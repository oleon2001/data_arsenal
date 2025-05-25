import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# crear_usuario para el login se crearon 2 usuarios
from core_app.models import User
 
email = "administrador@example.com"
password = "administrador"
name = "administrador"
last_name = "administrador"
type = "owner"

if not User.objects.filter(email=email).exists():
    User.objects.create_user(
        email=email,
        password=password,
        name=name,
        last_name=last_name,
        type=type
    )
    print("Usuario creado correctamente.")
else:
    print("El usuario ya existe.")