from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServicePlanViewSet, CompanyViewSet, UserViewSet, InvitationCodeViewSet,
    ReceptorViewSet, SensorViewSet, VehicleViewSet, SensorAssignmentViewSet,
    SensorReadingViewSet
)

# Crea un router y registra nuestros viewsets con él.
router = DefaultRouter()
router.register(r'service-plans', ServicePlanViewSet, basename='serviceplan')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'users', UserViewSet, basename='user')
router.register(r'invitation-codes', InvitationCodeViewSet, basename='invitationcode')
router.register(r'receptors', ReceptorViewSet, basename='receptor')
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'sensor-assignments', SensorAssignmentViewSet, basename='sensorassignment')
router.register(r'sensor-readings', SensorReadingViewSet, basename='sensorreading')

# Las URLs de la API son determinadas automáticamente por el router.
urlpatterns = [
    path('', include(router.urls)),
]
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
