from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('dashboard',Dashboard,basename="dashboard")
router.register('category',CategoryViewset,basename="category")
router.register('product',ProductViewset,basename="product")
router.register('order',OrderViewset,basename="order")
router.register('order_item',OrderItemViewset,basename="order_item")
router.register('order_delivery',OrderDeliveryViewset,basename="order_delivery")
router.register('purchase_item',PurchaseItemViewset,basename="purchase_item")
router.register('purchase',PurchaseViewset,basename="purchase")
router.register('purchase_delivery',PurchaseDeliveryViewset,basename="purchase_delivery")

urlpatterns = [
    path('',include(router.urls)),
]
