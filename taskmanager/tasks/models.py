from django.db import models

# Create your models here.

# Define choices as a tuple

PRIORITY_CHOICES = (
    ("LOW", "Low"),
    ("MED", "Medium"),
    ("HIGH", "High"),
)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default="LOW")

    def __str__(self):
        return self.title
