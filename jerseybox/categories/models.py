from django.db import models
import uuid
from django_countries.fields import CountryField


class Continent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class CountryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = CountryField(unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    flag_image_path = models.CharField(max_length=100,default=None)

    def __str__(self):
        return f"{self.country.name} ({self.country.code})"

    def country_flag_url(self):
        return f"/static/flags/{self.country.code.lower()}.png"


class League(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='league_logos/')

    def __str__(self):
        return self.name


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='club_logos/')

    def __str__(self):
        return self.name
