from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

class Account(models.Model):
    user        = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    info        = models.TextField(max_length=700, verbose_name=_('Info'), blank=True, null=True)
    birth_date  = models.DateField(verbose_name=_('Birth Date'), blank=True, null=True)

    def __str__(self):
        return '{0} - {0}'.format(self.user.username, self.user.email)

@receiver(post_save, sender=User)
def update_user_account(sender, instance, created, **kwargs):
    """Mise à jour de l'instance de user Account"""
    if created:
        # Une fois qu'une instance de User sera sauvegardée
        # Une instance de Account sera sauvegardée
        Account.objects.create(user=instance)
