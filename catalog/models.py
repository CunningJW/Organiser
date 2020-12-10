from django.db import models

# Create your models here.
class Conctract(models.Model):
    name = models.CharField(max_length=100, help_text="Enter a city name for a contract")
    zakupkiId = models.CharField(max_length=50, help_text="Enter an id from zakupki.gov.ru")


    def __str__(self):
        return self.title




class Task(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a task name")
    contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.title
