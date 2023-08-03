


from django.db import models

class Gender(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Continent(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Nation(models.Model):
    name = models.CharField(max_length=50)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=100)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Jersey(models.Model):
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    jersey_type = models.CharField(max_length=20, choices=[('Home', 'Home'), ('Away', 'Away')])

    def __str__(self):
        return f" {self.jersey_type} Jersey"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image1=models.ImageField(upload_to='product/',null=True)
    image2=models.ImageField(upload_to='product/',null=True)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price=models.DecimalField(max_digits=10, decimal_places=2)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # Add other product attributes as needed

    def __str__(self):
        return self.name
