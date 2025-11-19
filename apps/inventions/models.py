from django.db import models

# Create your models here.


class Invention(models.Model):
    class DangerLevel(models.IntegerChoices):
        VERY_LOW = 1, "Very Low"
        LOW = 2, "Low"
        MEDIUM = 3, "Medium"
        HIGH = 4, "High"
        EXTREME = 5, "Extreme"

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    usefulness_level = models.PositiveIntegerField(default=5)
    danger_level = models.IntegerField(
        choices=DangerLevel.choices,
        default=DangerLevel.MEDIUM,
    )
    for_students = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student_name = models.CharField(max_length=250, default=None)

    def __str__(self):
        return f"{self.name} (Usefulness: {self.usefulness_level}, Danger: {self.danger_level})"
