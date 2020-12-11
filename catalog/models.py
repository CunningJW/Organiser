from django.db import models

# Create your models here.
class Contract(models.Model):
    contractName = models.CharField(max_length=100, help_text="Enter a city name for a contract")
    zakupkiId = models.CharField(max_length=50, help_text="Enter an id from zakupki.gov.ru")
    dateStart = models.DateField()
    dateEnd = models.DateField()

    def __str__(self):
        return self.contractName
    def display_tasks(self):
        selfTasks = Task.objects.filter(contract__contractName='Cars')
        return ', '.join([task.taskName for task in selfTasks])

    class Meta:
        db_table = "Contract"

class Task(models.Model):
    taskName = models.CharField(max_length=200, help_text="Enter a task name")
    description = models.TextField(help_text="Enter a task description")
    contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True)
    datetimeStart = models.DateTimeField()
    datetimeEnd = models.DateTimeField()
    status = models.CharField(max_length=1, help_text="Enter a task status 0 - active, 1 - completed")

    def __str__(self):
        return self.taskName


class Document(models.Model):
    documentName = models.CharField(max_length=200, help_text="Enter a Document name")
    description = models.TextField(help_text="Enter a Document description")
    file = models.FileField(upload_to='uploads/')
    contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.documentName
