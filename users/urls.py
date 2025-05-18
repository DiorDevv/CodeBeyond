from django.urls import path

from .views import UserListView
from users.views import ConfirmationSendToEmailGenericAPIView, ForgotPasswordGenericAPIView, LoginView

urlpatterns = [
    path('user-send-email', ConfirmationSendToEmailGenericAPIView.as_view()),
    path('user-forget-password/<str:key>', ForgotPasswordGenericAPIView.as_view()),
    path('loign', LoginView.as_view(), name='login'),
    path('user-list', UserListView.as_view(), name='user-list'),

]
