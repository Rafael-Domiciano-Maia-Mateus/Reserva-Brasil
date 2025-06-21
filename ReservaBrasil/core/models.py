from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class UserApp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=20)
    id_user = models.AutoField(primary_key=True)

    def __str__(self):
        return f'Nome: {self.user.username}; E-mail: {self.user.email}; id: {self.id_user}'


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
    

class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)
    

class Property(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200)
    id_property = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    typeProperty = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Nome: {self.name}; Categoria: {self.category}; Tipo: {self.typeProperty}; id: {self.id_property}'


class Reservation(models.Model):
    pass
