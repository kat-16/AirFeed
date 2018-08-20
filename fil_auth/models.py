from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
class CustomUser(AbstractUser):
    is_ecoord = models.BooleanField(default = False)
    is_presenter = models.BooleanField(default = False)
    about = models.CharField(max_length = 1000)
    idf = models.CharField(max_length=64, verbose_name=u"Identification key",
                 default=uuid.uuid4())
