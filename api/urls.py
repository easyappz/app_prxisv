from django.urls import path
from .views import (
    HelloView,
    RegisterView,
    LoginView,
    MeView,
    MessagesListView,
    MessageCreateView
)

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("messages/", MessagesListView.as_view(), name="messages-list"),
    path("messages/", MessageCreateView.as_view(), name="message-create"),
]
