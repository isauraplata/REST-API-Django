from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
import json
from .models import Employee, CustomPermissions
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_http_methods



@login_required
@require_http_methods("GET")
def getAll(request):
    data = Employee.objects.all()
    serialized_data = serialize('json', data)
    parsed_data = json.loads(serialized_data)
    return JsonResponse(parsed_data, safe=False)



@login_required
@permission_required(CustomPermissions.CAN_CREATE_EMPLOYEE, raise_exception=True)
@require_http_methods("POST")
def create_employee(request):
    try:
        if not request.user.has_perm('reservations.can_create_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            first_name = body_data.get('first_name')
            last_name = body_data.get('last_name')
            email = body_data.get('email')
            phone_number = body_data.get('phone_number')
            hire_date = body_data.get('hire_date')
            position = body_data.get('position')
            salary = body_data.get('salary')
            is_active = body_data.get('is_active')
            hours_worked = body_data.get('hours_worked')
        
            new_employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            hire_date=hire_date,
            position=position,
            salary=salary,
            is_active=is_active,
            hours_worked=hours_worked,
            )

            new_employee.save()
            return HttpResponse("save succesfully")
    except IntegrityError:
        return HttpResponse("Error")


@login_required
@require_http_methods("DELETE")
def delete_employee(request, employee_id):
    try:
        if not request.user.has_perm('reservations.can_delete_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            employee = get_object_or_404(Employee, id=employee_id)
            employee.delete()
            return JsonResponse({'[message]': 'delete successfully!'}, status=200)       
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)
        


@login_required
@require_http_methods("PUT")
def update_employee(request, employee_id):
    try:
        if not request.user.has_perm('reservations.can_update_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            employee = get_object_or_404(Employee, id=employee_id)    
            employee.first_name = body_data.get('first_name', employee.first_name)
            employee.last_name = body_data.get('last_name',employee.last_name)
            employee.email = body_data.get('email',employee.email)
            employee.phone_number = body_data.get('phone_number',employee.phone_number)
            employee.hire_date = body_data.get('hire_date',employee.hire_date)
            employee.position = body_data.get('position',employee.position)
            employee.salary = body_data.get('salary',employee.salary)
            employee.is_active = body_data.get('is_active',employee.is_active)
            employee.hours_worked = body_data.get('hours_worked',employee.hours_worked)
            employee.save()
            return JsonResponse({'message': 'Update successful!'}, status=200)
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)