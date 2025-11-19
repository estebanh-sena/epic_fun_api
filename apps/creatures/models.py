from django.db import models


class Creature(models.Model):
    """
    Modelo para representar una criatura ridícula de estilo RPG.
    """

    class Rarity(models.TextChoices):
        COMMON = "common", "Common"
        RARE = "rare", "Rare"
        EPIC = "epic", "Epic"
        LEGENDARY = "legendary", "Legendary"

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    power_level = models.PositiveIntegerField(default=1)
    rarity = models.CharField(
        max_length=20,
        choices=Rarity.choices,
        default=Rarity.COMMON,
    )
    favorite_invention = models.ForeignKey(
        "inventions.Invention",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favored_by_creatures",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student_name = models.CharField(max_length=250, default=None)

    def __str__(self) -> str:
        return f"{self.name} ({self.rarity})"
