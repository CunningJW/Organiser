from django.shortcuts import render
from .models import Contract, Task, Document
from rest_framework import serializers, generics
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render


# Create your views here.

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id','contractName','zakupkiId','dateStart','dateEnd','display_tasks')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('taskName','description','taskContractName','datetimeStart','datetimeEnd','status')


def contractlink(request):
    return render(request, "tableofcontracts.html")

def tasklink(request):
    return render(request, "tableoftasks.html")

class ContractView(generics.ListAPIView):
    queryset = Contract.objects.all()
    def get(self, request):
        getCurrentUser(request)
        queryset = self.get_queryset()
        # template_name = 'tableofcontracts.html'
        contracts = Contract.objects.all()#filter(user = 'getCurrentUser(request)')
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

class ContractDetailView(generics.ListAPIView):
    def get_object(self, code):
        try:
            return Contract.objects.get(id = code)
        except:
            return Response(status=404)
    # queryset = Contract.objects.get(code = code)
    def get(self,request,code):
        contract = Contract.objects.get(id = code)
        queryset = self.get_queryset()
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

class TaskView(generics.ListAPIView):
    queryset = Task.objects.all()
    def get(self, request):
        getCurrentUser(request)
        getTasks()
        queryset = self.get_queryset()
        # template_name = 'tableofcontracts.html'
        tasks = Task.objects.all()#filter(user = 'getCurrentUser(request)')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

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
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

def getCurrentUser(request):
    return request.user

def getTasks():
    print(Task.objects.all())
# @api_view(['GET','POST'])
# def list_contract(request):
#     if request.method == "GET":
#         contract = Contract.objects.all()
#         serializer = ContractSerializer(contract, many = True)
#         return Response(serializer.data)
#     else:
#         serializer = ContractSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = 201)
#         return Response(serializer.errors, status = 400)

# @api_view(['GET','DELETE','PUT'])
# def contract_details(request, code):
#     try:
#         contract = Contract.objects.get(code=code)
#     except:
#         return Response(status=404)
#
#     if request.method == 'GET':
#         serializer = ContractSerializer(course)
#         return Response(serializer.data)
#     elif request.method == 'PUT':    # Update
#         serializer = ContractSerializer(contract, data=request.data)
#         if serializer.is_valid():
#            serializer.save()    # Update table in DB
#            return Response(serializer.data)
#
#         return Response(serializer.errors, status=400)  # Bad request
#     elif request.method == 'DELETE':
#         contract.delete()
#         return Response(status=204)

# @api_view(['GET','POST'])
# def list_task(request):
#     if request.method == "GET":
#         task = Task.objects.all()
#         serializer = TaskSerializer(task, many = True)
#         return Response(serializer.data)
#     else:
#         serializer = TaskSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = 201)
#         return Response(serializer.errors, status = 400)


def main(request):
    return render(
        request,
        'main.html',
    )
