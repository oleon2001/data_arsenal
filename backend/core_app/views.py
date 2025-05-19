from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import (
    ServicePlan, Company, User, InvitationCode,
    Receptor, Sensor, Vehicle, SensorAssignment, SensorReading,
)
from .serializers import (
    ServicePlanSerializer, CompanySerializer, UserSerializer, InvitationCodeSerializer,
    ReceptorSerializer, SensorSerializer, VehicleSerializer, SensorAssignmentSerializer,
    SensorReadingSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Puedes definir permisos más granulares si es necesario.
# Por ejemplo, IsAdminUser para ciertas acciones.
# from rest_framework.permissions import IsAdminUser

class ServicePlanViewSet(viewsets.ModelViewSet):
    queryset = ServicePlan.objects.all()
    serializer_class = ServicePlanSerializer
    # permission_classes = [permissions.IsAdminUser] # Ejemplo: Solo admins pueden gestionar planes

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # Añade lógica de permisos según sea necesario

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Considera permisos para quién puede listar/crear/modificar usuarios

class InvitationCodeViewSet(viewsets.ModelViewSet):
    queryset = InvitationCode.objects.all()
    serializer_class = InvitationCodeSerializer

class ReceptorViewSet(viewsets.ModelViewSet):
    queryset = Receptor.objects.all()
    serializer_class = ReceptorSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class SensorAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SensorAssignment.objects.all()
    serializer_class = SensorAssignmentSerializer

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all().order_by('-created_at') # Más recientes primero
    serializer_class = SensorReadingSerializer
    # Podrías querer permisos más estrictos o filtros aquí

@api_view(['GET'])
def misdatos_view(request):
    # Puedes devolver datos de ejemplo o consultar un modelo real
    data = [
        {"id": 1, "nombre": "Ejemplo 1", "descripcion": "Descripción de ejemplo 1"},
        {"id": 2, "nombre": "Ejemplo 2", "descripcion": "Descripción de ejemplo 2"},
    ]
    return Response(data)

# Create your views here.
