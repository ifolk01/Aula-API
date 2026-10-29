from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    genre = models.CharField(
        max_length=100,
        default="Não informado"
    )
    release_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title