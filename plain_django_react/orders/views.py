from django.shortcuts import render
from rest_framework import viewsets, serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    confirmed_at = serializers.DateTimeField(read_only=True)
    canceled_at = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    quote = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'created_at', 'confirmed_at', 'canceled_at', 'name', 'customer_order_number', 
            'customer', 'status', 'quote'
        ]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.with_api_annotations().all()

