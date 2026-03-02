from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

router = DefaultRouter()
router.register(r'orders', PaymentViewSet, basename='payment-order')

urlpatterns = [
    path('', include(router.urls)),
]
