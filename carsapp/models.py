from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('WAGON', 'WAGON')])
    year = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
