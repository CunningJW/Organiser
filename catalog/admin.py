from django.contrib import admin
from .model import Contract, Task

admin.user.register(Contract)
admin.user.register(Task)
# Register your models here.
