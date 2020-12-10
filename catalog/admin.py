from django.contrib import admin
from .models import Contract, Task

# Define the admin class
@admin.register(Contract)
class ContractAdmin (admin.ModelAdmin):
    list_display = ('zakupkiId','name','dateStart','dateEnd')

@admin.register(Task)
class TaskAdmin (admin.ModelAdmin):
    list_display = ('name','description','contract','datetimeStart','datetimeEnd','status')

class DocumentAdmin (admin.DocumentAdmin):
    list_display = ('name','description','file','contract')
# admin.site.register(Contract, ContractAdmin)
# admin.site.register(Contract)
#admin.site.register(Task)
# Register your models here.
