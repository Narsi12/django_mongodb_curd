from djongo import models

class Employee(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)