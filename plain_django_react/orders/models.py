from django.db import models
from django.utils import timezone
from .managers import OrderManager

# Create your models here.

class Order(models.Model):
    objects = OrderManager()
    class Status:
        PENDING = 'pending'
        CONFIRMED = 'confirmed'
        CANCELED = 'canceled'
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=50)
    customer_order_number = models.CharField(max_length=50, null=True, blank=True)

    def get_status(self):
        if self.canceled_at:
            return Order.Status.CANCELED
        if self.confirmed_at:
            return Order.Status.CONFIRMED
        return Order.Status.PENDING
    
    def confirm(self):
        """
        An order is confirmed by creating the OC and sending it to the customer.
        """
        self.confirmed_at = timezone.now()
        self.save(update_fields=['confirmed_at'])

    def cancel(self):
        if self.confirmed_at:
            raise Exception('Cannot cancel a confirmed order')
        self.canceled_at = timezone.now()
        self.save(update_fields=['canceled_at'])


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_line_items')
    product_description = models.CharField(max_length=50)
    position = models.PositiveSmallIntegerField()
    quantity = models.IntegerField()
    price_cents = models.DecimalField(max_digits=10, decimal_places=2)

