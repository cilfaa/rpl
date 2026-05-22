from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Bahan
from .nutrisi_service import hitung_dan_simpan_nutrisi_menu


@receiver(post_save, sender=Bahan)
def update_nutrisi_setelah_save(sender, instance, **kwargs):
    try:
        transaction.on_commit(
            lambda: hitung_dan_simpan_nutrisi_menu(instance.menu)
        )
    except Exception:
        pass


@receiver(post_delete, sender=Bahan)
def update_nutrisi_setelah_delete(sender, instance, **kwargs):
    try:
        transaction.on_commit(
            lambda: hitung_dan_simpan_nutrisi_menu(instance.menu)
        )
    except Exception:
        pass