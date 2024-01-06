from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee, CustomPermissions
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_http_methods


@csrf_exempt
@login_required
@require_http_methods("GET")
def getAll(request):
    data = Employee.objects.all()
    res = json.loads(serialize('json', data))
    return JsonResponse(res, safe=False)


@csrf_exempt
@login_required
@permission_required(CustomPermissions.CAN_CREATE_EMPLOYEE, raise_exception=True)
@require_http_methods("POST")
def create_employee(request):
    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
        position = request.POST.get('position')
        salary = request.POST.get('salary')
        is_active = request.POST.get('is_active')
        hours_worked = request.POST.get('hours_worked')
        user_id = request.user.id
        user_instance = User.objects.get(id=user_id)

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
            user=user_instance,
        )

        new_employee.save()
        return HttpResponse("save succesfully")
    except IntegrityError:
        return HttpResponse("Error")


@csrf_exempt
@login_required
@permission_required(CustomPermissions.CAN_DELETE_EMPLOYEE, raise_exception=True)
@require_http_methods("DELETE")
def delete_employee(request, employee_id):

    try:
        user = request.user
        pk = employee_id
        reservation = get_object_or_404(Employee, id=employee_id)
        reservation.delete()
        print(user)
        print(pk)
        return HttpResponse("delete successfully")
    except IntegrityError:
        return HttpResponse("Error")



@csrf_exempt
@login_required
@permission_required(CustomPermissions.CAN_UPDATE_EMPLOYEE, raise_exception=True)
@require_http_methods("PUT")
def update_employee(request, employee_id):

    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        employee = get_object_or_404(Employee, id=employee_id)
                
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
        position = request.POST.get('position')
        salary = request.POST.get('salary')
        is_active = request.POST.get('is_active')
        hours_worked = request.POST.get('hours_worked')
        

        employee.first_name = first_name if first_name is not None else employee.first_name
        employee.phone_number = phone_number if phone_number is not None else employee.phone_number
        
        employee.save()
        return HttpResponse("update successfully")
    except IntegrityError:
        return HttpResponse("Error")

