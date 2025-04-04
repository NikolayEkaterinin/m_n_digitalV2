from django.db import transaction
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Order


@receiver(m2m_changed, sender=Order.selected_options.through)
def update_prices_on_options_change(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.calculate_prices()
        instance.save(update_fields=['base_price',
                                     'options_price',
                                     'total_price'])
