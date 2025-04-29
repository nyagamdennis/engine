from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart, SalesAnalytics

@receiver(post_save, sender=Cart)
def update_sales_analytics(sender, instance, created, **kwargs):
    if created and instance.fully_payed:
        SalesAnalytics.update_monthly_sales()
