from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        if not request.data:
            return Response(
                {"error": "Request body is empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        username = request.data.get("username")
        password = request.data.get("password")

        user = None
        if "@" in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response(
            {"error": "username or password is wrong, please try agian"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_profile(request):
    username = request.user

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({"error": "No account was found with the provided username."}, status=status.HTTP_404_NOT_FOUND)

    serializer = RegisterSerializer(user)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_profile(request):
    user = request.user

    update_fields = {key: value for key, value in request.data.items()}
    if not update_fields:
        return Response(
            {"error": "No valid fields provided for update"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    unknown_fields = set(update_fields.keys()) - set(RegisterSerializer.Meta.fields)
    if unknown_fields:
        return Response(
            {"error": f"Unknown fields provided: {', '.join(unknown_fields)}"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    serializer = RegisterSerializer(user, data=update_fields, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)
