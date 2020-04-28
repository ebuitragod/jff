from django.db import models
import uuid

class User(models.Model):
    """
    Información básica de los usuarios.
    """
    name = models.CharField(max_length=40)
    email = models.EmailField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.name

class Store(models.Model):
    """
    sobre las tiendas que estén afiliadas
    """
    name = models.CharField(max_length = 40)
    bio = models.CharField(max_length=100)
    email = models.EmailField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.name

