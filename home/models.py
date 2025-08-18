from django.db import models

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
        
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    submmited_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"

class feedback(models.Model):
    comment = models.TextField()
    submmited_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"feedback {self.id} - {self.submmited_at.strtime('%Y-%m%d')}"
