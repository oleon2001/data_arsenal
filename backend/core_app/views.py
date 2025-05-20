# core_app/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Device, DeviceData
from .serializers import DeviceSerializer, DeviceDataSerializer, DeviceDataCreateSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Max, Min, Sum # Para agregaciones
from datetime import timedelta # Para filtros de tiempo

# Imports para alertas y correos
from django.conf import settings
from .email_utils import send_alert_email
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDataListCreateView(generics.ListCreateAPIView):
    queryset = DeviceData.objects.all().order_by('-timestamp') # Ordenar por más reciente
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeviceDataCreateSerializer
        return DeviceDataSerializer

    def perform_create(self, serializer):
        device_data = serializer.save()
        logger.debug(f"Nuevo DeviceData guardado: {device_data.id} para el dispositivo {device_data.device.name}")
        self.check_thresholds_and_alert(device_data)

    def check_thresholds_and_alert(self, device_data_instance):
        """
        Verifica si el valor del dato está fuera de los umbrales definidos
        y envía una alerta por correo si es necesario.
        """
        data_type = device_data_instance.data_type
        value = device_data_instance.data_value
        device = device_data_instance.device

        thresholds = settings.DEVICE_DATA_THRESHOLDS.get(data_type)

        if thresholds:
            min_val = thresholds.get('min')
            max_val = thresholds.get('max')
            alert_triggered = False
            alert_type = ""

            if min_val is not None and value < min_val:
                alert_triggered = True
                alert_type = "mínimo"
                logger.warning(
                    f"ALERTA: {device.name} - {device_data_instance.get_data_type_display()} ({value}) "
                    f"por debajo del mínimo ({min_val})."
                )
            elif max_val is not None and value > max_val:
                alert_triggered = True
                alert_type = "máximo"
                logger.warning(
                    f"ALERTA: {device.name} - {device_data_instance.get_data_type_display()} ({value}) "
                    f"por encima del máximo ({max_val})."
                )

            if alert_triggered:
                subject = f"Alerta de Umbral: {device_data_instance.get_data_type_display()} en {device.name}"
                context = {
                    'subject': subject,
                    'device_name': device.name,
                    'device_id': device.device_id,
                    'data_type_display': device_data_instance.get_data_type_display(),
                    'data_value': value,
                    'unit': device_data_instance.get_unit_display(),
                    'threshold_min': min_val if min_val is not None else "N/A",
                    'threshold_max': max_val if max_val is not None else "N/A",
                    'timestamp': device_data_instance.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z"),
                }
                html_content = render_to_string('alerts/threshold_alert_email.html', context)
                
                # Enviar correo
                # Puedes pasar una lista específica de destinatarios aquí si es necesario
                # o dejar que use la lista por defecto de settings.ALERT_EMAIL_RECIPIENTS
                send_alert_email(subject, html_content)
        else:
            logger.debug(f"No hay umbrales definidos para el tipo de dato: {data_type}")


class DeviceDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceData.objects.all()
    serializer_class = DeviceDataSerializer # Podrías querer usar DeviceDataCreateSerializer para 'PUT' si permites cambiar el 'device'

class DeviceSpecificDataListView(generics.ListAPIView):
    serializer_class = DeviceDataSerializer

    def get_queryset(self):
        """
        Devuelve los datos para un dispositivo específico, opcionalmente filtrados por tipo de dato
        y rango de fechas.
        """
        device_id_param = self.kwargs.get('device_id_param') # El nombre del parámetro en la URL
        device = get_object_or_404(Device, device_id=device_id_param) # Busca por device_id
        
        queryset = DeviceData.objects.filter(device=device).order_by('-timestamp')

        # Filtrar por tipo de dato si se provee en los query params
        data_type = self.request.query_params.get('type')
        if data_type:
            queryset = queryset.filter(data_type=data_type)

        # Filtrar por rango de fechas si se proveen en los query params
        # Ejemplo: /api/devices/DEVICE_ID_XYZ/data/?start_date=2023-01-01&end_date=2023-01-31
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if start_date_str:
            try:
                start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(timestamp__gte=start_date)
            except ValueError:
                # Manejar error de formato de fecha si es necesario
                pass 
        
        if end_date_str:
            try:
                end_date = timezone.datetime.strptime(end_date_str, "%Y-%m-%d").date()
                # Para incluir el día final, filtramos hasta el final de ese día
                end_date_plus_one = end_date + timedelta(days=1)
                queryset = queryset.filter(timestamp__lt=end_date_plus_one)
            except ValueError:
                pass

        return queryset

class DeviceDataAggregatesView(APIView):
    def get(self, request, device_id_param, data_type):
        device = get_object_or_404(Device, device_id=device_id_param)
        
        # Validar que data_type sea uno de los permitidos para evitar errores
        valid_data_types = [choice[0] for choice in DeviceData.DATA_TYPE_CHOICES]
        if data_type not in valid_data_types:
            return Response(
                {"error": f"Tipo de dato '{data_type}' no es válido. Válidos son: {', '.join(valid_data_types)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener el rango de tiempo para la agregación (últimas 24 horas por defecto)
        time_delta_hours = int(request.query_params.get('hours', 24)) # Permite personalizar via ?hours=X
        end_time = timezone.now()
        start_time = end_time - timedelta(hours=time_delta_hours)

        queryset = DeviceData.objects.filter(
            device=device,
            data_type=data_type,
            timestamp__gte=start_time,
            timestamp__lte=end_time
        )

        if not queryset.exists():
            return Response({
                "device_name": device.name,
                "device_id": device.device_id,
                "data_type": data_type,
                "period_hours": time_delta_hours,
                "message": "No data found for the specified period and data type.",
                "aggregates": None
            }, status=status.HTTP_200_OK) # O 404 si prefieres

        aggregates = queryset.aggregate(
            avg_value=Avg('data_value'),
            max_value=Max('data_value'),
            min_value=Min('data_value'),
            sum_value=Sum('data_value'), # Suma podría no tener sentido para todos los tipos
            count=models.Count('id') # Para saber cuántos registros se agregaron
        )
        
        # Formatear para mejor legibilidad, especialmente si los valores son None
        response_data = {
            "device_name": device.name,
            "device_id": device.device_id,
            "data_type": device.get_data_type_display() if hasattr(device, 'get_data_type_display') else data_type, # Mejorar esto
            "data_type_raw": data_type,
            "period_hours": time_delta_hours,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "unit": queryset.first().get_unit_display() if queryset.first() else "N/A", # Unidad del primer dato
            "aggregates": {
                "average": round(aggregates['avg_value'], 2) if aggregates['avg_value'] is not None else None,
                "maximum": aggregates['max_value'],
                "minimum": aggregates['min_value'],
                "sum": aggregates['sum_value'],
                "count": aggregates['count']
            }
        }

        return Response(response_data)

# Nueva vista para obtener el último dato de un tipo específico para un dispositivo
class LatestDeviceDataView(APIView):
    def get(self, request, device_id_param, data_type):
        device = get_object_or_404(Device, device_id=device_id_param)

        # Validar que data_type sea uno de los permitidos
        valid_data_types = [choice[0] for choice in DeviceData.DATA_TYPE_CHOICES]
        if data_type not in valid_data_types:
            return Response(
                {"error": f"Tipo de dato '{data_type}' no es válido. Válidos son: {', '.join(valid_data_types)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        latest_data = DeviceData.objects.filter(
            device=device,
            data_type=data_type
        ).order_by('-timestamp').first()

        if not latest_data:
            return Response({
                "message": f"No data found for device {device.name} and data type {data_type}."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = DeviceDataSerializer(latest_data)
        return Response(serializer.data)
