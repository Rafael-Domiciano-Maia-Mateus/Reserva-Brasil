from django.db import models
from django.contrib.auth.models import User

class UserApp(models.Model):
    """
    Extends the default Django User model with additional fields.

    Attributes:
        user (OneToOneField): Link to Django's built-in User model.
        phoneNumber (CharField): User's phone number.
        id_user (AutoField): Primary key for UserApp.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=20)
    id_user = models.AutoField(primary_key=True)

    def __str__(self):
        """
        Returns a string representation of the user with username, email and ID.
        """
        return f'Nome: {self.user.username}; E-mail: {self.user.email}; id: {self.id_user}'


class Category(models.Model):
    """
    Represents a property category (e.g., apartment, house, etc.).

    Attributes:
        name (CharField): The category name.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        """
        Returns the category name as its string representation.
        """
        return str(self.name)


class Type(models.Model):
    """
    Represents the type of property (e.g., rental, sale, commercial).

    Attributes:
        name (CharField): The type name.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        """
        Returns the type name as its string representation.
        """
        return str(self.name)


class Property(models.Model):
    """
    Represents a real estate property.

    Attributes:
        image (ImageField): Optional image of the property.
        name (CharField): Name of the property.
        id_property (AutoField): Primary key for Property.
        price (DecimalField): Price of the property.
        rate (DecimalField): Additional rate or fee.
        active (BooleanField): Whether the property is active/available.
        category (ForeignKey): Category this property belongs to.
        typeProperty (ForeignKey): Type of the property.
        description (TextField): Description of the property.
    """

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
        """
        Returns a string with the property's name, category, type, and ID.
        """
        return f'Nome: {self.name}; Categoria: {self.category}; Tipo: {self.typeProperty}; id do imóvel: {self.id_property}'


class Reservation(models.Model):
    """
    Represents a reservation made by a user for a property.

    Attributes:
        user (ForeignKey): The user who made the reservation.
        id_user (ForeignKey): Reference to UserApp (extended user profile).
        nameProperty (ForeignKey): The property reserved.
        category (ForeignKey): Category of the reserved property.
        typeProperty (ForeignKey): Type of the reserved property.
        checkin (DateField): Check-in date.
        checkout (DateField): Check-out date.
        id_reservation (AutoField): Primary key for Reservation.
        price (DecimalField): Price per day for the reservation.
        rate (DecimalField): Additional rate or fee applied.
    """

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
        """
        Calculates the total price of the reservation based on the number of days and rates.

        Returns:
            Decimal: Total price (price * number of days + rate).
        """
        days = (self.checkout - self.checkin).days
        return (self.price or 0) * days + (self.rate or 0)

    def __str__(self):
        """
        Returns a string representation with username, user ID, property name, and reservation ID.
        """
        return f'Nome: {self.user.username}; ID usuário: {self.id_user}; Nome do imóvel: {self.nameProperty}; ID do imovel: {self.id_reservation}'
