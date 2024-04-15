from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"", views.OrderViewSet, basename="orders")

urlpatterns = [
    path('tracking/', include('orders.orders_tracking.urls')),
    path('quotes/', include('orders.orders_quoting.urls')),
]

urlpatterns += router.urls
