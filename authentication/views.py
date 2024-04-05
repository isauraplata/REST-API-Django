from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from reservations.models import CustomPermissions as ReservationsCustomPermissions, Permission as ReservationsPermission
from orders.models import CustomPermissions as OrdersCustomPermissions, Permission as OrdersPermission
from authentication.validations import UserSignupSerializer
from rest_framework.decorators import api_view


@login_required
@api_view(['POST'])
def signout(request):
    logout(request)
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('csrftoken')
    response.delete_cookie('jwt')
    return response


@api_view(['POST'])
def signup(request):
    try:
        validation_serializer = UserSignupSerializer(data=request.data)
        if validation_serializer.is_valid():
            validated_data = validation_serializer.validated_data
            user = User.objects.create_user(**validated_data)

            # Agregar permisos al usuario
            user.user_permissions.add(ReservationsPermission.objects.get(
                codename=ReservationsCustomPermissions.CAN_CREATE_RESERVATION))

            user.user_permissions.add(ReservationsPermission.objects.get(
                codename=ReservationsCustomPermissions.CAN_DELETE_RESERVATION))

            user.user_permissions.add(ReservationsPermission.objects.get(
                codename=ReservationsCustomPermissions.CAN_UPDATE_RESERVATION))

            user.user_permissions.add(OrdersPermission.objects.get(
                codename=OrdersCustomPermissions.CAN_CREATE_ORDER))

            user.user_permissions.add(OrdersPermission.objects.get(
                codename=OrdersCustomPermissions.CAN_DELETE_ORDER))

            user.user_permissions.add(OrdersPermission.objects.get(
                codename=OrdersCustomPermissions.CAN_UPDATE_ORDER))

            user.save()
            login(request, user)
            return JsonResponse({'message': 'Account created successfully!'}, status=200)
        else:
            return JsonResponse(validation_serializer.errors, status=400)
    except IntegrityError:
        return JsonResponse({'[ERROR]': 'Email or username already in use'}, status=500)



@api_view(['POST'])
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

