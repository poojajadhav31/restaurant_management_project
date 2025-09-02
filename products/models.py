from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)   
    def __str__(self):
        return str(self.name)

class Special(models.Model):
    item_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - {self.date}"
    
class Chef(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chef_photos/', blank=True, null=True)

    def __str__(self):
        return str(self.name)