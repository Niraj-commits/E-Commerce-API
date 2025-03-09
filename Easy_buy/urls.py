from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('category',CategoryViewset,basename="category")
router.register('product',ProductViewset,basename="product")
router.register('order',OrderViewset,basename="order")
router.register('order_item',OrderItemViewset,basename="order_item")
router.register('delivery',DeliveryViewset,basename="delivery")

urlpatterns = [
    path('',include(router.urls)),
]
