from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    VEG = "veg"
    EGG = "egg"
    NONVEG = "nonveg"
    VEGAN = "vegan"
    DIET_CHOICES = [
        (VEG, "Vegetarian"),
        (EGG, "Eggetarian"),
        (NONVEG, "Non-vegetarian"),
        (VEGAN, "Vegan"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    diet_preference = models.CharField(max_length=10, choices=DIET_CHOICES, default=NONVEG)
    started_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class DailyEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    date = models.DateField()

    walked_km = models.DecimalField("Walk (km)", max_digits=4, decimal_places=1, default=Decimal("0.0"))
    brisk_included = models.BooleanField("Included a brisk stretch", default=False)

    mobility_done = models.BooleanField("Mobility warm-up done", default=False)

    strength_done = models.BooleanField("Strength session done", default=False)
    chair_squats_reps = models.PositiveSmallIntegerField(default=0)
    wall_pushups_reps = models.PositiveSmallIntegerField(default=0)
    glute_bridges_reps = models.PositiveSmallIntegerField(default=0)
    bird_dog_reps = models.PositiveSmallIntegerField(default=0)
    plank_seconds = models.PositiveSmallIntegerField(default=0)

    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal("0.0"))
    water_liters = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal("0.0"))
    protein_every_meal = models.BooleanField("Protein at every meal", default=False)
    did_anyway = models.BooleanField("Did it despite low motivation", default=False)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(fields=["user", "date"], name="one_entry_per_user_per_day"),
        ]

    def __str__(self):
        return f"{self.user.username} — {self.date}"

    @property
    def points(self):
        pts = 0
        if self.walked_km >= Decimal("2.0"):
            pts += 10
        if self.strength_done:
            pts += 10
        if self.mobility_done:
            pts += 5
        if self.protein_every_meal:
            pts += 5
        if Decimal("7.0") <= self.sleep_hours <= Decimal("9.0"):
            pts += 5
        if self.did_anyway:
            pts += 5
        return pts
