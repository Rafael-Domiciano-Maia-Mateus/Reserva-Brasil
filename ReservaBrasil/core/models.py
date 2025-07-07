from django.db import models
from django.contrib.auth.models import User


class UserApp(models.Model):
    """
    Extends the default Django User model with additional fields.
    """
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
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  
        blank=True,
        related_name="properties"
    )
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200)
    id_property = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    typeProperty = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=800, null=True, blank=True)

    def __str__(self):
        return f'Nome: {self.name}; Categoria: {self.category}; Tipo: {self.typeProperty}; id do imóvel: {self.id_property}'


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.ForeignKey(UserApp, on_delete=models.SET_NULL, null=True)
    nameProperty = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    typeProperty = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)
    checkin = models.DateField()
    checkout = models.DateField()
    id_reservation = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def priceTotal(self):
        days = (self.checkout - self.checkin).days
        return (self.price or 0) * days + (self.rate or 0)

    def __str__(self):
        return f'Nome: {self.user.username}; ID usuário: {self.id_user}; Nome do imóvel: {self.nameProperty}; ID do imovel: {self.id_reservation}'


class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)  
    beds = models.PositiveIntegerField(default=1)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    numberOfPeople = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.property.name}"
