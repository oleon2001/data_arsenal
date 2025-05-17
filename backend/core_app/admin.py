from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    ServicePlan, Company, User, InvitationCode,
    Receptor, Sensor, Vehicle, SensorAssignment, SensorReading
)

# Personalización del Admin para el modelo User (opcional pero recomendado)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'last_name', 'type', 'company', 'is_staff', 'deleted')
    list_filter = ('type', 'is_staff', 'deleted', 'company')
    search_fields = ('email', 'name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'last_name', 'phone', 'birthday', 'language')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'gr oups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined' if hasattr(User, 'date_joined') else 'created_at', 'renewal_date')}), # date_joined es de AbstractUser
        ('Company', {'fields': ('company', 'company_info', 'type')}),
        ('Status', {'fields': ('deleted',)}),
    )
    # add_fieldsets es para el formulario de creación de usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'name', 'last_name', 'type', 'company'),
        }),
    )
    # Para AbstractBaseUser, date_joined no existe por defecto, created_at es el análogo.
    # Si usaras AbstractUser, date_joined estaría disponible.
    readonly_fields = ('last_login', 'created_at', 'updated_at')


admin.site.register(User, UserAdmin)
admin.site.register(ServicePlan)
admin.site.register(Company)
admin.site.register(InvitationCode)
admin.site.register(Receptor)
admin.site.register(Sensor)
admin.site.register(Vehicle)
admin.site.register(SensorAssignment)
admin.site.register(SensorReading)
