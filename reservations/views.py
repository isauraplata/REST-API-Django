from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Reservation, CustomPermissions, Permission
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden


@csrf_exempt
@login_required
@require_http_methods("POST")
def signout(request):
    logout(request)
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('csrftoken')
    response.delete_cookie('jwt')
    return response


@csrf_exempt
@require_http_methods("POST")
def signup(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        username = body_data.get('username')
        email = body_data.get('email')
        password = body_data.get('password')

        user = User.objects.create_user(
            username=username, password=password, email=email)

        user.user_permissions.add(Permission.objects.get(
            codename=CustomPermissions.CAN_CREATE_RESERVATION))

        user.user_permissions.add(Permission.objects.get(
            codename=CustomPermissions.CAN_DELETE_RESERVATION))

        user.user_permissions.add(Permission.objects.get(
            codename=CustomPermissions.CAN_UPDATE_RESERVATION))

        user.save()
        login(request, user)
        return HttpResponse("Acount created succesfuly!")
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Email or username already in use'}, status=500)


@csrf_exempt
@require_http_methods("POST")
def signin(request):

    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        username = body_data.get('username')
        email = body_data.get('email')
        password = body_data.get('password')

        user = authenticate(
            request, username=username, password=password, email=email)

        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Establece la cookie con el token JWT
        response = JsonResponse({'token': access_token})
        response.set_cookie(key='jwt', value=access_token,
                            max_age=3600, httponly=True)
        return response
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)


@csrf_exempt
@login_required
@require_http_methods("GET")
def getAll(request):
    user_id = request.user.id
    user_reservation = Reservation.objects.filter(user_id=user_id)
    orders_json = json.loads(serialize('json', user_reservation))
    return JsonResponse(orders_json, safe=False)


@csrf_exempt
@login_required
@require_http_methods("POST")
def create_reservations(request):
    try:

        if not request.user.has_perm('reservations.can_create_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            customer = body_data.get('customer')
            customer_phone = body_data.get('customer_phone')
            customer_email = body_data.get('customer_email')
            special_notes = body_data.get('special_notes')
            reservation_date = body_data.get('reservation_date')
            location = body_data.get('location')
            hour = body_data.get('hour')
            num_people = body_data.get('num_people')
            user_id = request.user.id
            user_instance = User.objects.get(id=user_id)
            
            new_reservation = Reservation(
            customer=customer,
            customer_phone=customer_phone,
            customer_email=customer_email,
            special_notes=special_notes,
            reservation_date=reservation_date,
            location=location,
            hour=hour,
            num_people=num_people,
            user=user_instance,
        )
            
        new_reservation.save()
        return HttpResponse("save succesfully!")
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)


@csrf_exempt
@login_required
@require_http_methods("DELETE")
def delete_reservation(request, reservation_id):
    try:
        if not request.user.has_perm('reservations.can_delete_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.delete()
            return JsonResponse({'[message]': 'delete successfully!'}, status=200)       
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)


@csrf_exempt
@login_required
@require_http_methods("PUT")
def update_reservation(request, reservation_id):
    try:

        if not request.user.has_perm('reservations.can_update_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else: 
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            customer = body_data.get('customer')
            customer_phone = body_data.get('customer_phone')
            customer_email = body_data.get('customer_email')
            special_notes = body_data.get('special_notes')
            reservation_date = body_data.get('reservation_date')
            location = body_data.get('location')
            hour = body_data.get('hour')
            num_people = body_data.get('num_people')
            status = body_data.get('status')
            
            reservation = get_object_or_404(Reservation, id=reservation_id)

            reservation.customer = customer if customer is not None else reservation.customer

            reservation.customer_phone = customer_phone if customer_phone is not None else reservation.customer_phone

            reservation.location = location if location is not None else reservation.location

            reservation.customer_email = customer_email if customer_email is not None else reservation.customer_email

            reservation.special_notes = special_notes if special_notes is not None else reservation.special_notes

            reservation.reservation_date = reservation_date if reservation_date is not None else reservation.reservation_date

            reservation.hour = hour if hour is not None else reservation.hour

            reservation.num_people = num_people if num_people is not None else reservation.num_people

            reservation.status = status if status is not None else reservation.status

            reservation.save()
            return JsonResponse({'[message]': 'update successfully!'}, status=200)  
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)



