import os
import resend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Inicializa el cliente de Resend con la API key
# Es importante que RESEND_API_KEY esté configurada en tus settings (idealmente desde variables de entorno)
try:
    resend.api_key = settings.RESEND_API_KEY
except AttributeError:
    logger.error("RESEND_API_KEY no está configurada en settings.py. Los correos no se enviarán.")
    resend.api_key = None # Evita errores si no está configurada, pero no enviará correos


def send_alert_email(subject, html_content, recipient_list=None):
    """
    Envía un correo electrónico de alerta utilizando Resend.

    Args:
        subject (str): El asunto del correo.
        html_content (str): El contenido HTML del correo.
        recipient_list (list, optional): Lista de destinatarios. 
                                         Si es None, usará settings.ALERT_EMAIL_RECIPIENTS.
    
    Returns:
        bool: True si el correo se envió (o se intentó enviar), False si hubo un error de configuración.
    """
    if not resend.api_key:
        logger.error("No se puede enviar el correo: RESEND_API_KEY no está configurada.")
        return False

    if recipient_list is None:
        recipient_list = settings.ALERT_EMAIL_RECIPIENTS

    if not recipient_list:
        logger.warning("No hay destinatarios configurados para las alertas por correo.")
        return False

    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        params = {
            "from": from_email,
            "to": recipient_list,
            "subject": subject,
            "html": html_content,
        }
        email = resend.Emails.send(params)
        logger.info(f"Correo de alerta enviado a {recipient_list}. ID de Resend: {email.get('id')}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo de alerta con Resend: {e}")
        return False

# Ejemplo de cómo podrías usarlo (esto no se ejecuta directamente aquí):
# if __name__ == '__main__':
# # Esto es solo para prueba local si ejecutas este archivo directamente
# # Necesitarías configurar Django settings o mockearlos
#     class MockSettings:
#         RESEND_API_KEY = "tu_api_key_real_de_resend" # ¡No subas esto a Git!
#         DEFAULT_FROM_EMAIL = "tu_email_verificado@resend.dev"
#         ALERT_EMAIL_RECIPIENTS = ["destinatario_prueba@example.com"]
#
#     settings.configure(default_settings=MockSettings()) # Simulación básica
#     django.setup() # Necesario si usas plantillas Django
#
#     send_alert_email(
#         subject="Prueba de Alerta de Temperatura",
#         html_content="<h1>Alerta!</h1><p>La temperatura ha superado el umbral.</p>",
#     )
