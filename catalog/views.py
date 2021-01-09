from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from .serializers import *

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
        users = User.objects.all()
        # serializer = ContractSerializer(contracts, many=True)
        return Response({'contracts': contracts, 'users': users})

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
        ourDict = {}
        contract_id=Contract.objects.get(pk=pk)
        tasks = Task.objects.filter(taskContractName = pk)
        for i in contract_id.currentUsers.all():
             ourDict[i] = Task.objects.filter(performer = i)
        print(ourDict)
        documents = Document.objects.filter(contract = pk)
        serializer = ContractSerializer(contract_id)
        return Response({'serializer': serializer,'contract_id': contract_id, 'tasks' : tasks, 'documents' : documents, 'userTasks' : ourDict})

class TaskAddNew(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasksPlus.html'

    queryset = Task.objects.all()
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
