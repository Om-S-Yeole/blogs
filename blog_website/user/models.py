from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    subscription_preference = models.BooleanField(default=False)
    terms_and_privacy_policy_acceptance = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"