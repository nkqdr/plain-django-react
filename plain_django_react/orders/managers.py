from django.db import models

class _OrderBaseManager(models.Manager):
    def create(self, **kwargs):
        order = super().create(**kwargs)
        order.name = f"OC{order.id:08d}"
        order.save(update_fields=["name"])
        return order

class _OrderQuerySet(models.QuerySet):
    def with_api_annotations(self):
        return self.annotate(
            status=models.Case(
                models.When(canceled_at__isnull=False, then=models.Value("CANCELED")),
                models.When(confirmed_at__isnull=False, then=models.Value("CONFIRMED")),
                default=models.Value("PENDING"),
            )
        )

OrderManager = _OrderBaseManager.from_queryset(_OrderQuerySet)
