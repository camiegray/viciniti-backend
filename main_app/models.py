from django.contrib.auth.models import AbstractUser
from django.db import models

# User with roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('provider', 'Provider'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    location = models.CharField(max_length=255, blank=True)  # Optional string location


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField()
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")

    def __str__(self):
        return f"{self.title} - {self.provider.username}"


class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer.username} booked {self.service.title} at {self.datetime}"


class DiscountRule(models.Model):
    provider = models.OneToOneField(User, on_delete=models.CASCADE, related_name="discount_rule")
    radius_km = models.FloatField(default=5.0)
    group_size = models.IntegerField(default=2)
    discount_percent = models.FloatField(default=10.0)

    def __str__(self):
        return f"{self.provider.username}'s Discount Rule"
