from django.db import models

class feedback(models.Model):
    comment = models.TextField()
    submmited_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"feedback {self.id} - {self.submmited_at.strtime('%Y-%m%d')}"
