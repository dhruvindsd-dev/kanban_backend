from venv import create

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from rest_framework.authtoken.models import Token


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="data")

    phone = models.IntegerField(max_length=12, unique=True, blank=True, null=True)
    profile_img = ResizedImageField(
        size=[100, 100],
        upload_to="account/profile_img",
        crop=["middle", "center"],
        quality=80,
        keep_meta=False,
        force_format="PNG",
        default=None,
        null=True,
        blank=True,
    )

    @property
    def profile_img_url(self):
        if self.profile_img and self.profile_img.file:
            return self.profile_img.file.url
        return None

    def __str__(self) -> str:
        return f"[{self.role}] {self.get_full_name() } : {self.email}"


@receiver(post_save, sender=User)
def createUserData(sender, instance=None, created=False, **kwargs):
    if created:
        UserData.objects.create(user=instance)
        Token.objects.create(user=instance)
