from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User class
    """
    
    @property
    def name(self):
        if self.first_name and self.last_name:
            return "{0} {1}".format(self.first_name, self.last_name)
        else:
            return self.username