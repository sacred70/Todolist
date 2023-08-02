from django.urls import path

from views import VerificationCodeView

urlpatterns = [
    path('verify', VerificationCodeView.as_view()),
]
