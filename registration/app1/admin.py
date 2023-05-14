from django.contrib import admin
from .models import UserRegistration

# Register your models here.
@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'city' ,'present_address' , 'parmanent_address', 'user_profile_image')