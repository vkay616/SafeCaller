from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from .models import Contact, RegisteredUser, SpamReport
from .serializers import ContactSerializer, RegisteredUserSerializer, SpamReportSerializer, RegisteredUserLogoutSerializer, RegisteredUserLoginSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import django_filters
from .filters import ContactFilter


class RegisteredUserRegisterView(generics.CreateAPIView):
    queryset = RegisteredUser.objects.all()
    serializer_class = RegisteredUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.validated_data["hashed_password"] = make_password(
            serializer.validated_data["hashed_password"])
        serializer.save()


class RegisteredUserLoginView(generics.CreateAPIView):
    serializer_class = RegisteredUserLoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        number = request.data.get("number")
        password = request.data.get("hashed_password")
        print(number)
        print(password)
        print(make_password(password))
        user = RegisteredUser.objects.filter(number=number).first()
        print(check_password(password, user.hashed_password))
        if user:
            print(user.hashed_password)
            if check_password(password, user.hashed_password):
                RegisteredUser.objects.exclude(
                    id=user.id).update(is_logged_in=False)
                user.is_logged_in = True
                user.save()
                return Response({"message": "logged in successfully"})
            else:
                return Response({"error": "invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "phone number is not registered"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisteredUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = RegisteredUser.objects.filter(is_logged_in=True).first()

        if user:
            return (user, None)
        else:
            raise AuthenticationFailed("Log/Register to view")

    def authenticate_header(self, request):
        return "User logged in"


class IsUserLoggedIn(BasePermission):
    def has_permission(self, request, view):
        user = RegisteredUser.objects.filter(is_logged_in=True).first()
        return user is not None


class ContactListView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    authentication_classes = [RegisteredUserAuthentication]
    permission_classes = [IsUserLoggedIn]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ContactFilter


class SpamReportView(generics.CreateAPIView):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    authentication_classes = [RegisteredUserAuthentication]
    permission_classes = [IsUserLoggedIn]


class RegisteredUserLogoutView(generics.CreateAPIView):
    serializer_class = RegisteredUserLogoutSerializer
    authentication_classes = [RegisteredUserAuthentication]
    permission_classes = [IsUserLoggedIn]

    def post(self, request):

        user = RegisteredUser.objects.filter(is_logged_in=True).first()

        if user:
            # logout the user
            user.is_logged_in = False
            user.save()

            return Response({"message": "logged out successfully"})
        else:
            return Response({"error": "no user is logged in"}, status=status.HTTP_401_UNAUTHORIZED)