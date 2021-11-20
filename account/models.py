from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True,verbose_name='آدرس ایمیل')
    is_author = models.BooleanField(default=False,verbose_name="وضعیت نویسندگی")
    special_user = models.DateTimeField(default=timezone.now, verbose_name = "کاربر ویژه تا ")
    first_name = models.CharField(max_length=20, verbose_name="نام")
    last_name = models.CharField(max_length=20, verbose_name="نام خانوادگی")
    def is_special_user(self):
        if self.special_user >timezone.now():
            return True
        else:
            return False
    is_special_user.boolean =True
    is_special_user.short_description ="کاربر ویژه"