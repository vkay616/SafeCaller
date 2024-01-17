from django.urls import path
from .views import RegisteredUserRegisterView, RegisteredUserLoginView, RegisteredUserLogoutView, ContactListView, SpamReportView

urlpatterns = [
    path("register/", RegisteredUserRegisterView.as_view(), name="register-user"),
    path("login/", RegisteredUserLoginView.as_view(), name="login-user"),
    path("logout/", RegisteredUserLogoutView.as_view(), name="logout-user"),
    path("contacts/", ContactListView.as_view(), name="contact-list"),
    path("report/", SpamReportView.as_view(), name="report"),
]
