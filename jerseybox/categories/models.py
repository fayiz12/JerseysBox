from django.db import models
import uuid
from django_countries.fields import CountryField


class Continent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    continent_id = models.ForeignKey(Continent, on_delete=models.CASCADE)
    code = CountryField(unique=True)
    


class League(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    logo=models.ImageField(upload_to='league_logos/')

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    league_id = models.ForeignKey(League, on_delete=models.CASCADE)
    logo=models.ImageField(upload_to='club_logos/')