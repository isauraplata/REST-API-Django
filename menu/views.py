from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Dish, CustomPermissions
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden


@csrf_exempt
@login_required
@require_http_methods("GET")
def get_menu(request):
    data = Dish.objects.all()
    serialized_data = serialize('json', data)
    parsed_data = json.loads(serialized_data)
    return JsonResponse(parsed_data, safe=False)


@csrf_exempt
@login_required
@require_http_methods("POST")
def create_dish(request):
    try:
        if not request.user.has_perm('menu.can_create_dish'):
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
            image_path=image.name if image else None,
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
@require_http_methods("POST")
def update_dish(request, dish_id):
    try:
        if not request.user.has_perm('menu.can_update_dish'):
            return HttpResponseForbidden("You do not have enough permissions!")
        else:
            dish = get_object_or_404(Dish, id=dish_id)
            dish.name = request.POST.get("name", dish.name)
            dish.description = request.POST.get("description", dish.description)
            dish.category = request.POST.get("category", dish.category)
            dish.price = request.POST.get("price", dish.price)
            dish.availability = request.POST.get("availability", dish.availability)
            dish.ingredients = request.POST.get("ingredients", dish.ingredients)
            dish.allergens = request.POST.get("allergens", dish.allergens)
            dish.cuisine_type = request.POST.get("cuisine_type", dish.cuisine_type)
            dish.spice_level = request.POST.get("spice_level", dish.spice_level)
            dish.image = request.FILES.get("image", dish.image)
            dish.save()
            return JsonResponse({'[message]': 'update successfully!'}, status=200)
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Something goes wrong!'}, status=401)