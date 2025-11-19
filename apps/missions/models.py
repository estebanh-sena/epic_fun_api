from django.db import models


class Mission(models.Model):
    """
    Model that represents a funny RPG-style mission for students.
    """

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    title = models.CharField(max_length=150)  # Short mission title
    description = models.TextField()  # Detailed mission description

    difficulty = models.CharField(  # Difficulty level
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )

    xp_reward = models.PositiveIntegerField(
        default=10
    )  # XP reward for completing the mission
    is_active = models.BooleanField(default=True)  # Can this mission be assigned?

    # Relations with other apps
    recommended_excuse = models.ForeignKey(
        "excuses.Excuse",  # Related excuse to use if student fails
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="missions_with_excuse",
    )
    required_invention = models.ForeignKey(
        "inventions.Invention",  # Required impossible invention for the mission
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="missions_with_invention",
    )
    main_enemy = models.ForeignKey(
        "creatures.Creature",  # Main creature to face in the mission
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="missions_with_creature",
    )

    times_assigned = models.PositiveIntegerField(
        default=0
    )  # How many times this mission was assigned
    times_completed = models.PositiveIntegerField(
        default=0
    )  # How many times it was completed

    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp
    student_name = models.CharField(max_length=250, default=None)

    def __str__(self) -> str:
        return f"{self.title} ({self.difficulty})"
