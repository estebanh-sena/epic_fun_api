from django.db import models

# Create your models here.


class Excuse(models.Model):
    class Category(models.TextChoices):
        WORK = "work", "Work"
        STUDY = "study", "Study"
        MIXED = "mixed", "Mixed"

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.STUDY,
    )

    power_level = models.PositiveBigIntegerField(default=1)
    times_used = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student_name = models.CharField(max_length=250, default=None)

    def __str__(self):
        return f"{self.title} ({self.category})"
