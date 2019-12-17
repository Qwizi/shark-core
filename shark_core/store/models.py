from django.db import models
from .bonuses import bonus_manager


class Bonus(models.Model):
    BONUS_CHOICES = bonus_manager.get_bonus_choices()

    name = models.CharField(max_length=64, blank=False)
    tag = models.CharField(
        max_length=32,
        choices=BONUS_CHOICES,
        default=BONUS_CHOICES[0][0],
        blank=False,
        unique=True
    )

    def __str__(self):
        return '{} - {}'.format(self.name, self.get_tag_display())