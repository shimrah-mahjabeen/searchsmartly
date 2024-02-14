from django.db import models

# Create your models here.
class PointOfInterest(models.Model):
    internal_ID = models.AutoField(primary_key=True)
    external_ID = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    category = models.CharField(max_length=255)
    avg_rating = models.FloatField()

    def __str__(self):
        return self.name