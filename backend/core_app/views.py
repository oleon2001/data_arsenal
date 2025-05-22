# core_app/views.py

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes # Para vistas de función
from rest_framework.permissions import IsAuthenticated # Para proteger vistas
from rest_framework.authtoken.models import Token # Para el login con token
from django.contrib.auth import authenticate # Para el login

from .models import (
    Device, DeviceData, ServicePlan, Company, User, InvitationCode,
    Receptor, Sensor, Vehicle, SensorAssignment, SensorReading
)
from .serializers import (
    DeviceSerializer, DeviceDataSerializer, DeviceDataCreateSerializer,
    ServicePlanSerializer, CompanySerializer, UserSerializer, InvitationCodeSerializer,
    ReceptorSerializer, SensorSerializer, VehicleSerializer, SensorAssignmentSerializer,
    SensorReadingSerializer
)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Max, Min, Sum, Count
from datetime import timedelta

from django.conf import settings
from .email_utils import send_alert_email
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

# --- ViewSets ---

class ServicePlanViewSet(viewsets.ModelViewSet):
    queryset = ServicePlan.objects.all()
    serializer_class = ServicePlanSerializer
    # permission_classes = [IsAuthenticated] # Descomenta si necesitas proteger este ViewSet

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated] # Considera los permisos para la creación de usuarios

class InvitationCodeViewSet(viewsets.ModelViewSet):
    queryset = InvitationCode.objects.all()
    serializer_class = InvitationCodeSerializer
    # permission_classes = [IsAuthenticated]

class ReceptorViewSet(viewsets.ModelViewSet):
    queryset = Receptor.objects.all()
    serializer_class = ReceptorSerializer
    # permission_classes = [IsAuthenticated]

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    # permission_classes = [IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    # permission_classes = [IsAuthenticated]

class SensorAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SensorAssignment.objects.all()
    serializer_class = SensorAssignmentSerializer
    # permission_classes = [IsAuthenticated]

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    # permission_classes = [IsAuthenticated]


# --- Vistas para Device y DeviceData ---

class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]

class DeviceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]

class DeviceDataListCreateView(generics.ListCreateAPIView):
    queryset = DeviceData.objects.all().order_by('-timestamp')
    # permission_classes = [IsAuthenticated] # Proteger la creación de datos

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeviceDataCreateSerializer
        return DeviceDataSerializer

    def perform_create(self, serializer):
        # Asignar el dispositivo basado en el usuario autenticado o alguna otra lógica si es necesario
        # Por ejemplo, si el dispositivo está vinculado al usuario o a su compañía:
        # serializer.save(device=self.request.user.device_profile.device) # Ejemplo conceptual
        device_data = serializer.save()
        logger.debug(f"Nuevo DeviceData guardado: {device_data.id} para el dispositivo {device_data.device.name if device_data.device else 'Desconocido'}")
        if device_data.device:
            self.check_thresholds_and_alert(device_data)
        else:
            logger.warning(f"DeviceData {device_data.id} creado sin un dispositivo asociado.")

    def check_thresholds_and_alert(self, device_data_instance):
        data_type = device_data_instance.data_type
        value = device_data_instance.data_value
        device = device_data_instance.device

        thresholds_config = getattr(settings, 'DEVICE_DATA_THRESHOLDS', {})
        thresholds = thresholds_config.get(data_type)

        if thresholds:
            min_val = thresholds.get('min')
            max_val = thresholds.get('max')
            alert_triggered = False
            alert_type = ""
            unit_display = device_data_instance.get_unit_display()

            if min_val is not None and value < min_val:
                alert_triggered = True
                alert_type = "mínimo"
                logger.warning(
                    f"ALERTA: {device.name} - {device_data_instance.get_data_type_display()} ({value} {unit_display}) "
                    f"por debajo del mínimo ({min_val} {unit_display})."
                )
            elif max_val is not None and value > max_val:
                alert_triggered = True
                alert_type = "máximo"
                logger.warning(
                    f"ALERTA: {device.name} - {device_data_instance.get_data_type_display()} ({value} {unit_display}) "
                    f"por encima del máximo ({max_val} {unit_display})."
                )

            if alert_triggered:
                subject = f"Alerta de Umbral: {device_data_instance.get_data_type_display()} en {device.name}"
                context = {
                    'subject': subject,
                    'device_name': device.name,
                    'device_id': device.device_id,
                    'data_type_display': device_data_instance.get_data_type_display(),
                    'data_value': value,
                    'unit': unit_display,
                    'threshold_min': min_val if min_val is not None else "N/A",
                    'threshold_max': max_val if max_val is not None else "N/A",
                    'alert_type': alert_type,
                    'timestamp': device_data_instance.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z"),
                }
                html_content = render_to_string('alerts/threshold_alert_email.html', context)
                send_alert_email(subject, html_content)
        else:
            logger.debug(f"No hay umbrales definidos para el tipo de dato: {data_type}")


class DeviceDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceData.objects.all()
    serializer_class = DeviceDataSerializer
    # permission_classes = [IsAuthenticated]

class DeviceSpecificDataListView(generics.ListAPIView):
    serializer_class = DeviceDataSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        device_id_param = self.kwargs.get('device_id_param')
        device = get_object_or_404(Device, device_id=device_id_param)
        
        queryset = DeviceData.objects.filter(device=device).order_by('-timestamp')
        data_type = self.request.query_params.get('type')
        if data_type:
            queryset = queryset.filter(data_type=data_type)

        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if start_date_str:
            try:
                start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(timestamp__gte=start_date)
            except ValueError:
                pass 
        
        if end_date_str:
            try:
                end_date = timezone.datetime.strptime(end_date_str, "%Y-%m-%d").date()
                end_date_plus_one = end_date + timedelta(days=1)
                queryset = queryset.filter(timestamp__lt=end_date_plus_one)
            except ValueError:
                pass
        return queryset

class DeviceDataAggregatesView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, device_id_param, data_type):
        device = get_object_or_404(Device, device_id=device_id_param)
        
        valid_data_types = [choice[0] for choice in DeviceData.DATA_TYPE_CHOICES]
        if data_type not in valid_data_types:
            return Response(
                {"error": f"Tipo de dato '{data_type}' no es válido. Válidos son: {', '.join(valid_data_types)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        time_delta_hours = int(request.query_params.get('hours', 24))
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
            }, status=status.HTTP_200_OK)

        aggregates = queryset.aggregate(
            avg_value=Avg('data_value'),
            max_value=Max('data_value'),
            min_value=Min('data_value'),
            sum_value=Sum('data_value'),
            count=Count('id')
        )
        
        first_data_point = queryset.first()
        unit_display = first_data_point.get_unit_display() if first_data_point else "N/A"
        data_type_display = first_data_point.get_data_type_display() if first_data_point else data_type

        response_data = {
            "device_name": device.name,
            "device_id": device.device_id,
            "data_type_display": data_type_display,
            "data_type_raw": data_type,
            "period_hours": time_delta_hours,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "unit": unit_display,
            "aggregates": {
                "average": round(aggregates['avg_value'], 2) if aggregates['avg_value'] is not None else None,
                "maximum": aggregates['max_value'],
                "minimum": aggregates['min_value'],
                "sum": aggregates['sum_value'],
                "count": aggregates['count']
            }
        }
        return Response(response_data)

class LatestDeviceDataView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, device_id_param, data_type):
        device = get_object_or_404(Device, device_id=device_id_param)
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

# --- Vistas de función para login y datos de usuario ---

@api_view(['POST'])
def login_view(request):
    """
    Autentica a un usuario y devuelve un token.
    Espera 'email' y 'password' en el cuerpo de la solicitud.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Por favor, proporcione email y contraseña'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password) # username es email por USERNAME_FIELD

    if user is not None:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user) # Para devolver datos del usuario
            return Response({
                'token': token.key,
                'user': user_serializer.data # Devuelve información del usuario
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Esta cuenta está inactiva.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Solo usuarios autenticados pueden acceder
def misdatos_view(request):
    """
    Devuelve los datos del usuario autenticado.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
# Aquí puedes agregar más vistas de función según sea necesario
# --- Fin de las vistas de función ---
# --- Fin de las vistas de Device y DeviceData ---
# --- Fin de los ViewSets ---
# --- Fin de las vistas de función ---
# --- Fin de las vistas de función ---
# --- Fin de las vistas de función ---
# --- Fin de las vistas de función ---
# --- Fin de las vistas de función ---
# --- Fin de las vistas de función ---
# --- Fin de las vistas de función ---
# --- Fin de las vistas de función ---
