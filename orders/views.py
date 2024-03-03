from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order
from .models import Dish
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden


@csrf_exempt
@login_required
@require_http_methods("GET")
def get_orders(request):
    user_id = request.user.id
    user_orders = Order.objects.filter(user_id=user_id)
    orders_json = json.loads(serialize('json', user_orders))
    return JsonResponse(orders_json, safe=False)

@csrf_exempt
@login_required
@require_http_methods("POST")
def create_order(request):
    try:
        
        if not request.user.has_perm('orders.can_create_order'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            dish_id = body_data.get('dish_id')
            total_price = body_data.get('total_price')
            quantity = body_data.get('quantity')
            user_id = request.user.id
            user_instance = User.objects.get(id=user_id)
            dish_instance = Dish.objects.get(id=dish_id)

            new_order = Order(
            dish=dish_instance,
            quantity=quantity,
            total_price= total_price,
            user=user_instance,
            )
            
            new_order.save()
            return JsonResponse({'[message]': 'save successfully!'}, status=200)
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)


@csrf_exempt
@login_required
@require_http_methods("DELETE")
def delete_order(request, order_id):
    try:
        if not request.user.has_perm('orders.can_delete_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return JsonResponse({'[message]': 'delete successfully!'}, status=200)
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)


@csrf_exempt
@login_required
@require_http_methods("PUT")
def update_order(request, order_id):
    try:
        if not request.user.has_perm('orders.can_update_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            order = get_object_or_404(Order, id=order_id)
            order.dish_id = body_data.get('dish_id', order.dish_id)
            order.quantity = body_data.get('quantity', order.quantity)
            order.save()
            return JsonResponse({'message': 'Update successful!'}, status=200)
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)

