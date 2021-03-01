from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    """
    Profile model
    Proxy Model that extends the base data with other information.
    """
    # Relation to table user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    aadhar_uid = models.CharField(max_length=16, blank=False, null =False)
    biography = models.TextField(blank=True)

    face_picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )


    def __str__(self):
        """Return username"""
        return self.user.username