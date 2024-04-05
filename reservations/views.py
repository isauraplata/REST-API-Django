from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from django.http import HttpResponseForbidden
from reservations.models import Reservation
from rest_framework.decorators import api_view

@login_required
@api_view(['GET'])
def getAll(request):
    user_id = request.user.id
    user_reservation = Reservation.objects.filter(user_id=user_id)
    orders_json = json.loads(serialize('json', user_reservation))
    return JsonResponse(orders_json, safe=False)


@login_required
@api_view(['POST'])
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


@login_required
@api_view(['DELETE'])
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



@login_required
@api_view(['PUT'])
def update_reservation(request, reservation_id):
    try:
        if not request.user.has_perm('reservations.can_update_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)

            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.customer = body_data.get(
                'customer', reservation.customer)
            reservation.customer_phone = body_data.get(
                'customer_phone', reservation.customer_phone)
            reservation.customer_email = body_data.get(
                'customer_email', reservation.customer_email)
            reservation.special_notes = body_data.get(
                'special_notes', reservation.special_notes)
            reservation.reservation_date = body_data.get(
                'reservation_date', reservation.reservation_date)
            reservation.location = body_data.get(
                'location', reservation.location)
            reservation.hour = body_data.get('hour', reservation.hour)
            reservation.num_people = body_data.get(
                'num_people', reservation.num_people)
            reservation.status = body_data.get('status', reservation.status)
            reservation.save()
            return JsonResponse({'message': 'Update successful!'}, status=200)
    except IntegrityError:
        return JsonResponse({'error': 'Something went wrong!'}, status=401)
