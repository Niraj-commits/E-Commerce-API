from django.urls import path
from .views import *

urlpatterns = [
    path('register/customer',CustomerRegisterView.as_view()),
    path('register/supplier',SupplierRegisterView.as_view()),
    path('register/delivery',DeliveryRegisterView.as_view()),
    path('login/',LoginView.as_view()),
]
