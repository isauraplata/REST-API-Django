from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Dish, CustomPermissions, Permission
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden


@csrf_exempt
@login_required
@require_http_methods("GET")
def get_menu(request):
    data = Dish.objects.all()
    res = json.loads(serialize('json', data))
    return JsonResponse(res, safe=False)

@csrf_exempt
@login_required
@require_http_methods("POST")
def create_dish(request):
    try:
        if not request.user.has_perm('reservations.can_create_dish'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            name = request.POST.get("name")
            description = request.POST.get("description")
            category = request.POST.get("category")
            price = request.POST.get("price")
            availability = request.POST.get("availability")
            ingredients = request.POST.get("ingredients")
            allergens = request.POST.get("allergens")
            cuisine_type = request.POST.get("cuisine_type")
            spice_level = request.POST.get("spice_level")
            image = request.FILES.get("image")

            user_id = request.user.id
            user_instance = User.objects.get(id=user_id)

            new_dish = Dish(
            name=name,
            description=description,
            category=category,
            price=price,
            availability=availability,
            ingredients=ingredients,
            allergens=allergens,
            cuisine_type=cuisine_type,
            spice_level=spice_level,
            image=image,
            user=user_instance,
            )
            
            new_dish.save()
            return JsonResponse({'[message]': 'Save successfully!'}, status=200) 
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)


@csrf_exempt
@login_required
@require_http_methods("DELETE")
def delete_dish(request, dish_id):
    try:
        if not request.user.has_perm('reservations.can_delete_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            dish = get_object_or_404(Dish, id=dish_id)
            dish.delete()
            return JsonResponse({'[message]': 'delete successfully!'}, status=200) 
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)


@csrf_exempt
@login_required
@require_http_methods("PUT")
def update_dish(request, dish_id):
    try:
        if not request.user.has_perm('reservations.can_update_reservation'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            dish = get_object_or_404(Dish, id=dish_id)
            name = request.POST.get("name")
            description = request.POST.get("description")
            category = request.POST.get("category")
            price = request.POST.get("price")
            availability = request.POST.get("availability")
            ingredients = request.POST.get("ingredients")
            allergens = request.POST.get("allergens")
            cuisine_type = request.POST.get("cuisine_type")
            spice_level = request.POST.get("spice_level")
            image = request.FILES.get("image")
        
            dish.name = name if name is not None else dish.customer
            dish.description = description if description is not None else dish.description
            dish.price = price if price is not None else dish.price
        
            dish.save()
            return JsonResponse({'[message]': 'update successfully!'}, status=200)  
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)
