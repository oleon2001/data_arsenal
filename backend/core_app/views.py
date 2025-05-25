# core_app/views.py

# Django imports
from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import get_object_or_404 # Comentado si no se usa directamente
# from django.utils import timezone # Comentado si no se usa directamente
# from datetime import datetime # Comentado si no se usa directamente

# Django REST framework imports
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import views
from rest_framework.authtoken.models import Token

# Local imports
from .models import (
    User,
    Company,
    ServicePlan,
    InvitationCode,
    Receptor,
    Sensor,
    Vehicle,
    SensorAssignment,
    SensorReading,
    Device,
    DeviceData,
    # Los siguientes modelos no están en el models.py proporcionado y han sido comentados:
    # Planta, Area, Linea, Equipo, PuntoMonitoreo,
    # Variable, UnidadMedida, ValorVariable, Limite, Alerta, Reporte,
    # Notificacion, Rol, Permiso, UsuarioRol, RolPermiso
)
from .serializers import (
    UserSerializer,
    CompanySerializer,
    ServicePlanSerializer,
    InvitationCodeSerializer,
    ReceptorSerializer,
    SensorSerializer,
    VehicleSerializer,
    SensorAssignmentSerializer,
    SensorReadingSerializer,
    DeviceSerializer,
    DeviceDataSerializer, # Asegúrate que este es el nombre correcto
    DeviceDataCreateSerializer, # Añadido para la creación
    LoginSerializer,
    UserRegistrationSerializer,
    # Los siguientes serializadores corresponden a modelos comentados y han sido comentados:
    # PlantaSerializer, AreaSerializer, LineaSerializer, EquipoSerializer,
    # PuntoMonitoreoSerializer, VariableSerializer, UnidadMedidaSerializer,
    # ValorVariableSerializer, LimiteSerializer, AlertaSerializer, ReporteSerializer,
    # NotificacionSerializer, RolSerializer, PermisoSerializer,
)
# from .email_utils import send_threshold_alert_email # Comentado ya que su uso depende de modelos ahora comentados

import logging

logger = logging.getLogger(__name__)


# Vista para el registro de usuarios
@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration_view(request):
    """
    Registra un nuevo usuario en el sistema.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "Usuario registrado exitosamente.",
            "user_id": user.id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para el login de usuarios
class LoginView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            logger.info(f"Intento de login para el usuario: {email}")

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"Login exitoso para el usuario: {email}")
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(user)
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': 'Login exitoso'
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Fallo de login para el usuario: {email}. Credenciales inválidas o usuario inactivo.")
                try:
                    from django.contrib.auth.models import User
                    user_exists = User.objects.filter(username=email).exists()
                    if not user_exists:
                        logger.warning(f"El usuario '{email}' no existe.")
                        return Response({'error': 'Credenciales inválidas.', 'detail': f"El usuario '{email}' no existe."}, status=status.HTTP_401_UNAUTHORIZED)
                    user_obj = User.objects.get(username=email)
                    if not user_obj.is_active:
                        logger.warning(f"El usuario '{email}' está inactivo.")
                        return Response({'error': 'Cuenta de usuario inactiva.', 'detail': f"La cuenta para '{email}' está inactiva."}, status=status.HTTP_401_UNAUTHORIZED)
                    return Response({'error': 'Credenciales inválidas.', 'detail': 'Nombre de usuario o contraseña incorrectos.'}, status=status.HTTP_401_UNAUTHORIZED)
                except User.DoesNotExist:
                    logger.error(f"Error inesperado al buscar el usuario '{email}' después de un fallo de autenticación.")
                    return Response({'error': 'Error del servidor.', 'detail': 'Ocurrió un error inesperado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    logger.error(f"Excepción no manejada durante el fallo de login para '{email}': {str(e)}")
                    return Response({'error': 'Error del servidor.', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.warning(f"Datos de login inválidos: {serializer.errors}")
        return Response({'error': 'Datos inválidos.', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Cierra la sesión del usuario y elimina su token de autenticación.
    """
    from rest_framework.authtoken.models import Token # <--- Importación local de Token
    try:
        # auth_token es el related_name por defecto para el token del usuario
        if hasattr(request.user, 'auth_token') and request.user.auth_token:
             request.user.auth_token.delete()
    except (AttributeError, Token.DoesNotExist): 
        pass
    logout(request)
    return Response({'message': 'Cierre de sesión exitoso.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def misdatos_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# ViewSets para los modelos definidos en models.py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='me')
    def mis_datos_action(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class ServicePlanViewSet(viewsets.ModelViewSet):
    queryset = ServicePlan.objects.all()
    serializer_class = ServicePlanSerializer
    permission_classes = [IsAuthenticated]

class InvitationCodeViewSet(viewsets.ModelViewSet):
    queryset = InvitationCode.objects.all()
    serializer_class = InvitationCodeSerializer
    permission_classes = [IsAuthenticated]

class ReceptorViewSet(viewsets.ModelViewSet):
    queryset = Receptor.objects.all()
    serializer_class = ReceptorSerializer
    permission_classes = [IsAuthenticated]

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class SensorAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SensorAssignment.objects.all()
    serializer_class = SensorAssignmentSerializer
    permission_classes = [IsAuthenticated]

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all().order_by('-created_at')
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticated]

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

class DeviceDataViewSet(viewsets.ModelViewSet):
    queryset = DeviceData.objects.all().order_by('-timestamp')
    # Determinar el serializador basado en la acción (GET vs POST/PUT)
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DeviceDataCreateSerializer
        return DeviceDataSerializer
    permission_classes = [IsAuthenticated]


# --- ViewSets y Vistas Comentadas (Dependen de Modelos No Encontrados) ---
# class PlantaViewSet(viewsets.ModelViewSet):
#     queryset = Planta.objects.all()
#     serializer_class = PlantaSerializer
#     permission_classes = [IsAuthenticated]

# class AreaViewSet(viewsets.ModelViewSet):
#     queryset = Area.objects.all()
#     serializer_class = AreaSerializer
#     permission_classes = [IsAuthenticated]

# class LineaViewSet(viewsets.ModelViewSet):
#     queryset = Linea.objects.all()
#     serializer_class = LineaSerializer
#     permission_classes = [IsAuthenticated]

# class EquipoViewSet(viewsets.ModelViewSet):
#     queryset = Equipo.objects.all()
#     serializer_class = EquipoSerializer
#     permission_classes = [IsAuthenticated]

# class PuntoMonitoreoViewSet(viewsets.ModelViewSet):
#     queryset = PuntoMonitoreo.objects.all()
#     serializer_class = PuntoMonitoreoSerializer
#     permission_classes = [IsAuthenticated]

# class VariableViewSet(viewsets.ModelViewSet):
#     queryset = Variable.objects.all()
#     serializer_class = VariableSerializer
#     permission_classes = [IsAuthenticated]

# class UnidadMedidaViewSet(viewsets.ModelViewSet):
#     queryset = UnidadMedida.objects.all()
#     serializer_class = UnidadMedidaSerializer
#     permission_classes = [IsAuthenticated]

# class ValorVariableViewSet(viewsets.ModelViewSet):
#     queryset = ValorVariable.objects.all().order_by('-timestamp')
#     serializer_class = ValorVariableSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         valor_variable = serializer.save()
#         # self.check_variable_limits(valor_variable) # Lógica de límites comentada

#     def check_variable_limits(self, valor_variable_instance):
#         # ... (lógica comentada que depende de Limite, Alerta, etc.) ...
#         pass

# class LimiteViewSet(viewsets.ModelViewSet):
#     queryset = Limite.objects.all()
#     serializer_class = LimiteSerializer
#     permission_classes = [IsAuthenticated]

# class AlertaViewSet(viewsets.ModelViewSet):
#     queryset = Alerta.objects.all().order_by('-timestamp')
#     serializer_class = AlertaSerializer
#     permission_classes = [IsAuthenticated]

# class ReporteViewSet(viewsets.ModelViewSet):
#     queryset = Reporte.objects.all()
#     serializer_class = ReporteSerializer
#     permission_classes = [IsAuthenticated]

# class NotificacionViewSet(viewsets.ModelViewSet):
#     queryset = Notificacion.objects.all()
#     serializer_class = NotificacionSerializer
#     permission_classes = [IsAuthenticated]

# class RolViewSet(viewsets.ModelViewSet):
#     queryset = Rol.objects.all()
#     serializer_class = RolSerializer
#     permission_classes = [IsAuthenticated]

# class PermisoViewSet(viewsets.ModelViewSet):
#     queryset = Permiso.objects.all()
#     serializer_class = PermisoSerializer
#     permission_classes = [IsAuthenticated]


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def monitor_view(request):
#     return Response({"message": "Monitor view necesita ser actualizada con los modelos correctos."}, status=status.HTTP_501_NOT_IMPLEMENTED)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def check_limits_view(request):
#     return Response({"message": "Check limits view necesita ser actualizada con los modelos correctos."}, status=status.HTTP_501_NOT_IMPLEMENTED)

