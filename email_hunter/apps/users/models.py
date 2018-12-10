from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User class
    """
    
    @property
    def name(self):
        return "{0} {1}".format(self.first_name, self.last_name)