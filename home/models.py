from django.db import models

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    opening_hours = models.TextField(blank=True)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class RestaurantLocation(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} - {self.zip_code}"
        
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    submmited_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class feedback(models.Model):
    comment = models.TextField()
    submmited_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"feedback {self.id} - {self.submmited_at.strtime('%Y-%m%d')}"

python manage.py makemigrations
python manage.py migrate