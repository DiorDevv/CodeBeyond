from random import randint

from django.core.cache import cache

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from shared.funksions import send_verifications
from users.models import CustomUser
from users.serializers import EmailSerializers, PasswordSerializer, UserSerializer

from rest_framework.response import Response
from .serializers import LoginSerializer


# Create your views here.

class ConfirmationSendToEmailGenericAPIView(GenericAPIView):
    serializer_class = EmailSerializers
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Agar foydalanuvchi mavjud bo‘lsa, yubormaymiz
        if CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        code = randint(100000, 999999)
        data = {
            'code': str(code),
            'username': serializer.validated_data['username'],
            'email': email,
            'password': serializer.validated_data['password'],
        }
        cache.set(email, data, timeout=300)  # 5 daqiqa
        send_verifications(email=email, message=f"tasdiqlash kodingiz {code}")
        return Response({
            "detail": "Activation email sent.",
            "code": "user_created",
        })


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        data = cache.get(email)

        if not data:
            return Response({"detail": "Verification code expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)

        if code != data.get('code'):
            return Response({"detail": "Incorrect code."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove code and extract password
        data.pop('code')
        password = data.pop('password')

        # Create and save the user with hashed password
        user = CustomUser.objects.create(**data)
        user.set_password(password)
        user.save()

        return Response({"detail": "User successfully created."}, status=status.HTTP_201_CREATED)


class ForgotPasswordGenericAPIView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PasswordSerializer

    def post(self, request, key, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = cache.get(serializer.validated_data.get('email'))
        if not email:
            raise ValidationError({"error": "not Found"})

        user = self.get_queryset().filter(email=email).first()
        if not user:
            raise ValidationError({"error": "User not Found"})

        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response("Success")



class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]