from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.required_params import require_params

# Create your views here.


# Create your views here.
@api_view(["POST"])
@require_params(["firstName", "lastName", "email", "username", "phone", "password"])
def register(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data["firstName"],
            last_name=data["lastName"],
            email=data["email"],
            username=data["username"],
            password=make_password(data["password"]),
        )
        if "phone" in data:
            user.data.phone = data["phone"]

    except IntegrityError as e:
        print(e)
        if "username" in str(e):
            return Response("username", status=status.HTTP_409_CONFLICT)
        if "phone" in str(e):
            return Response("phone number", status=status.HTTP_409_CONFLICT)

    return Response(
        {
            "firstName": user.first_name,
            "token": Token.objects.get_or_create(user=user)[0].key,
        }
    )


@api_view(["POST"])
@require_params(["emailOrPhone", "password"])
def login(request):
    data = request.data
    user = None
    try:
        user = User.objects.get(
            Q(email=data["emailOrPhone"].strip())
            | Q(username=data["emailOrPhone"].strip())
        )
    except:
        pass
    if user:
        pwd_valid = check_password(data["password"], user.password)
        if pwd_valid:
            return Response(
                { "firstName": user.first_name, "token": Token.objects.get_or_create(user=user)[0].key, }
            )
    return Response("No user found", status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@require_params(["img"])
def upload_img(request):
    data = request.data
    user = request.user
    user.data.profile_img = data["img"]
    user.data.save()
    return Response(user.data.profile_img.url)


