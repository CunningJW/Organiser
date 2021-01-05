from rest_framework import serializers
from .models import Contract, Task, Document
from django.contrib.auth.models import User


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id','contractName','zakupkiId','dateStart','dateEnd','display_tasks','getLink','linkToZakupkigov','currentUsers')

class TaskListSerializer(serializers.ModelSerializer):
    taskContractName = serializers.StringRelatedField()
    performer = serializers.StringRelatedField()
    sender = serializers.StringRelatedField()
    class Meta:
        model = Task
        fields = ('taskName','performer','sender','description','taskContractName','datetimeStart','datetimeEnd','status')

class DocumentGetSerializer(serializers.ModelSerializer):
    contract = serializers.StringRelatedField()
    class Meta:
        model = Document
        fields = ('documentName', 'description', 'file', 'contract')

class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('taskName','performer','description','taskContractName','datetimeStart','datetimeEnd')

class TaskPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('taskName','performer','sender','description','taskContractName','datetimeStart','datetimeEnd','status')

class DocumentSerializer(serializers.ModelSerializer):
    # file = serializers.FileField()
    class Meta:
        model = Document
        fields = ('documentName','description','file','contract')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
