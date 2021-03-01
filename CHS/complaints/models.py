from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Complaint(models.Model):

    DEFAULT_CATEGORY = (
        ('0.1', 'No mask'),
        ('0.5', 'No mask + Symptomatic'),
        ('0.9', 'No mask + Symptomatic + Unhygienic')
    )
    profile = models.ForeignKey(Profile, related_name="complaints", null=True, on_delete=models.SET_NULL )

    created_at = models.DateTimeField(auto_now=True)
    complaint_face_picture = models.ImageField(
        upload_to='complaints/pictures',
        blank=True,
        null=True
    )
    category = models.CharField(max_length = 30, choices=DEFAULT_CATEGORY)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('complaints:single', kwargs={'username': self.user.username,
                                              'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'complaint_face_picture']