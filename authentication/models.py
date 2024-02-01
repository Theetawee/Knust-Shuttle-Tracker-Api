from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    program = models.CharField(max_length=50, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="users/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'UserProfile'):
        User_Profile.objects.create(user=instance)