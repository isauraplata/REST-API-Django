from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone

    
    
class CustomPermissions:
    CAN_CREATE_EMPLOYEE = 'can_create_employee'
    CAN_DELETE_EMPLOYEE = 'can_delete_employee'
    CAN_UPDATE_EMPLOYEE = 'can_update_employee'
    
        
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField()
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()
    
    def calculate_salary(self, hourly_rate):
        """
        Calcula el salario del empleado basado en las horas trabajadas y la tarifa por hora.
        """
        return self.hours_worked * hourly_rate
    
    @staticmethod
    def create_custom_permissions():
        content_type = ContentType.objects.get_for_model(Employee)

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_CREATE_EMPLOYEE,
            name='Can create employee',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_DELETE_EMPLOYEE,
            name='Can delete employee',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_UPDATE_EMPLOYEE,
            name='Can update employee',
            content_type=content_type,
        )
        
    