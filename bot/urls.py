from django.urls import path

from bot import views

app_name = 'bot'

urlpatterns = [
    # Bot
    path('verify', views.VerificationCodeView.as_view(), name='verify'),
]
