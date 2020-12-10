from django.db import models

# Create your models here.
class Conctract(models.Model):
    name = models.CharField(max_length=100, help_text="Enter a city name for a contract")
    zakupkiId = models.CharField(max_length=50, help_text="Enter an id from zakupki.gov.ru")
    dateStart = models.DateField()
    dateEnd = models.DateField()

    def __str__(self):
        return self.title




class Task(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a task name")
    description = models.TextField(help_text="Enter a task description")
    contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True)
    datetimeStart = models.DateTimeField()
    datetimeEnd = models.DateTimeField()
    status = models.CharField(max_length=1, , help_text="Enter a task status")

    def __str__(self):
        return self.title
