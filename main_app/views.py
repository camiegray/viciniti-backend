from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .models import Service, Appointment, DiscountRule
from .serializers import (
    UserSerializer, ServiceSerializer, 
    AppointmentSerializer, DiscountRuleSerializer
)

User = get_user_model()

class Home(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Viciniti API!"})


# --- AUTH ---

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        refresh = RefreshToken.for_user(request.user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(request.user).data
        })


# --- PROVIDER ROUTES ---

class ServiceList(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "provider":
            raise PermissionDenied("Only providers can view services.")
        return Service.objects.filter(provider=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role != "provider":
            raise PermissionDenied("Only providers can create services.")
        serializer.save(provider=self.request.user)


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Service.objects.filter(provider=self.request.user)


class DiscountRuleListCreate(generics.ListCreateAPIView):
    serializer_class = DiscountRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DiscountRule.objects.filter(provider=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role != "provider":
            raise PermissionDenied("Only providers can create discount rules.")
        serializer.save(provider=self.request.user)


# --- CUSTOMER ROUTES ---

class AppointmentListCreate(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "customer":
            return Appointment.objects.filter(customer=self.request.user)
        elif self.request.user.role == "provider":
            return Appointment.objects.filter(service__provider=self.request.user)
        else:
            return Appointment.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "customer":
            raise PermissionDenied("Only customers can book appointments.")
        serializer.save(customer=self.request.user)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user.role == "customer":
            return Appointment.objects.filter(customer=self.request.user)
        elif self.request.user.role == "provider":
            return Appointment.objects.filter(service__provider=self.request.user)
        else:
            return Appointment.objects.none()
