# Este archivo se crea manualmente DENTRO de la carpeta core_app/migrations/
# después de crear la aplicación y ANTES de ejecutar makemigrations por primera vez para los modelos.
# O, alternativamente, puedes ejecutar makemigrations primero para los modelos,
# y luego crear una nueva migración vacía (python manage.py makemigrations --empty core_app)
# y añadir estas operaciones.
#
# Para la extensión pgcrypto, Django tiene una operación incorporada.
# Para el tipo ENUM, si bien Django lo maneja con CharField y choices,
# si necesitas el tipo ENUM a nivel de base de datos, puedes usar RunSQL.
# Sin embargo, para `user_type`, ya hemos usado TextChoices en el modelo,
# lo cual es la forma preferida en Django y no requiere un ENUM a nivel de DB
# a menos que tengas una razón específica para ello (ej. interoperabilidad con otras
# aplicaciones que leen directamente de la DB y esperan ese tipo ENUM).

from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

class Migration(migrations.Migration):

    # Esta migración debe ejecutarse ANTES de la migración que crea las tablas
    # que dependen de 'pgcrypto' o del tipo 'user_type' si se definiera aquí.
    # Sin embargo, con el modelo User usando TextChoices y UUIDField usando uuid.uuid4,
    # estas operaciones SQL directas podrían no ser estrictamente necesarias
    # para que los modelos de Django funcionen, pero se incluyen para seguir
    # de cerca tu script SQL original si es un requisito.

    # Si vas a definir modelos que usan `gen_random_uuid()` directamente en sus
    # `default` SQL (lo cual no es el enfoque de Django ORM), entonces `pgcrypto` es crucial.
    # Para el `user_type ENUM`, si no lo defines aquí, el `CharField` con `choices`
    # funcionará bien, pero la columna en la DB será `varchar`.

    # Por lo general, es mejor dejar que Django maneje la creación de tipos y defaults
    # a través de sus campos de modelo.

    dependencies = [
        # No hay dependencias iniciales si es la primera migración de la app.
        # Si ya tienes una migración '0001_initial.py' generada por Django
        # para tus modelos, esta migración debería ir ANTES de ella o
        # las operaciones se pueden fusionar.
        # Por simplicidad, si esta es la *primera* migración de `core_app`, está bien.
    ]

    operations = [
        CreateExtension('pgcrypto'), # Habilita la extensión pgcrypto
        # migrations.RunSQL(
        #     sql="CREATE TYPE user_type AS ENUM ('owner','admin','standard');",
        #     reverse_sql="DROP TYPE IF EXISTS user_type;"
        # ),
        # Nota: La creación del tipo ENUM 'user_type' mediante RunSQL se comenta
        # porque hemos definido User.UserType como TextChoices en models.py.
        # Django manejará la validación a nivel de aplicación.
        # Si necesitas el tipo ENUM explícito en PostgreSQL por otras razones,
        # puedes descomentar la operación RunSQL.
    ]
