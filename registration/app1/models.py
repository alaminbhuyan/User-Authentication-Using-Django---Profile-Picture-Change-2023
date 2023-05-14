from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class UserRegistration(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    present_address = models.CharField(max_length=200, null=True)
    parmanent_address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    user_profile_image = models.ImageField(verbose_name="Your profile image", upload_to='profileImages', default="avater.png", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.user_profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (210, 210)
            img.thumbnail(size=output_size)
            img.save(self.user_profile_image.path)