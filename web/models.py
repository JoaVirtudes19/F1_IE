from django.db import models

# Create your models here.




class Driver(models.Model):
    name = models.CharField(max_length=200,unique=True)
    code = models.CharField(max_length=3,null=True)
    driver_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Circuit(models.Model):
    name = models.CharField(max_length=200,unique=True)
    circuit_id = models.IntegerField()
    
    def __str__(self) -> str:
        return self.name