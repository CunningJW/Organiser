from django.shortcuts import render, redirect
from .models import Contract, Task, Document
from rest_framework import serializers, generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser

from rest_framework.views import APIView

# Create your views here.
########################################################################

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id','contractName','zakupkiId','dateStart','dateEnd','display_tasks','getLink','linkToZakupkigov','currentUsers')

class TaskListSerializer(serializers.ModelSerializer):
    taskContractName = serializers.StringRelatedField()
    performer = serializers.StringRelatedField()
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
#######################################################################
def getCurrentUser(request):
    return request.user

def main(request):
    return render(request,'main.html')


#######################################################################

class ContractView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    template_name = 'tableofcontracts.html'

    def get(self, request):
        contracts = Contract.objects.filter(currentUsers = getCurrentUser(request))
        # contracts = Contract.objects.all()
        users = User.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response({'serializer': serializer,'contracts': contracts, 'users': users})

class ContractDetailView(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "contractTemplate.html"

    def get_object(self, pk):
        try:
            contract_id=Contract.objects.get(pk=pk)
            tasks = Task.objects.filter(taskContractName = pk)
        except Contract.DoesNotExist:
            raise Http404("Contract does not exist")

    def get(self,request,pk):
        contract_id=Contract.objects.get(pk=pk)
        tasks = Task.objects.filter(taskContractName = pk)
        documents = Document.objects.filter(contract = pk)
        serializer = ContractSerializer(contract_id)
        return Response({'serializer': serializer,'contract_id': contract_id, 'tasks' : tasks, 'documents' : documents})


class ContractFilteringView(generics.ListAPIView):
    def get_object(self, request):
        try:
            return Contract.objects.filter(currentUsers = getCurrentUser(request))
        except:
            return Response(status=404)
    queryset = Contract.objects.all()
    def get(self,request):
        contract = Contract.objects.filter(currentUsers = getCurrentUser(request))
        queryset = self.get_queryset()
        serializer = ContractSerializer(contract, many=True)
        return Response(serializer.data)


class TaskAddNew(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasksPlus.html'
    # serializer_class = TaskPostSerializer

    def get(self, request):
        contracts = Contract.objects.all()
        users = User.objects.all()
        serializer = TaskGetSerializer()
        return Response({'serializer': serializer,'contracts': contracts, 'users': users})

    def post(self, request):
        request.data._mutable = True
        request.data['sender'] = str(getCurrentUser(request).id)
        request.data['status'] = str(0)
        request.data._mutable = False
        print(request.data)
        serializer = TaskPostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('myTasks')
        else:
            return Response(serializer.errors)




class TaskUserFilteringView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tableoftasks.html'

    def get_object(self, request):
        try:
            return Task.objects.filter(performer = getCurrentUser(request)).order_by('taskContractName')
        except:
            return Response(status=404)
    queryset = Task.objects.all()
    def get(self,request):
        myTasks = Task.objects.filter(performer = getCurrentUser(request)).order_by('taskContractName__contractName')
        queryset = self.get_queryset()
        serializer = TaskListSerializer(myTasks, many=True)
        return Response({'serializer': serializer,'tasks': myTasks})



class TaskDetailView(generics.ListAPIView):
    def get_object(self, code):
        try:
            return Task.objects.filter(taskContractName = code)
        except:
            return Response(status=404)
    queryset = Task.objects.all()
    def get(self,request,code):
        task = Task.objects.filter(taskContractName = code)
        queryset = self.get_queryset()
        serializer = TaskListSerializer(task, many=True)
        return Response(serializer.data)

class DocumentView(APIView):
    # queryset = Document.objects.all()
    # serializer_class = DocumentSerializer
    renderer_classes = [MultiPartParser,TemplateHTMLRenderer]
    template_name = 'documentPlus.html'

    def get(self, request):
        document = Document.objects.all()
        serializer = DocumentSerializer()
        return Response({'serializer' : serializer, 'document' : document})

    def post(self, request):
        serializer = DocumentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('myTasks')
        else:
            print("err")
            return Response(serializer.errors)
