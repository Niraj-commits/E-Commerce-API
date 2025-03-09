from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('category',CategoryViewset,basename="category")
router.register('product',ProductViewset,basename="product")
router.register('order',OrderViewset,basename="order")

urlpatterns = [
    path('',include(router.urls)),
]
