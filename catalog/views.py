from django.shortcuts import render
from .models import Contract, Task, Document
from rest_framework import serializers, generics, mixins
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
########################################################################

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id','contractName','zakupkiId','dateStart','dateEnd','display_tasks','getLink','linkToZakupkigov')

class TaskGetSerializer(serializers.ModelSerializer):
    taskContractName = serializers.StringRelatedField()
    followers = serializers.StringRelatedField()
    class Meta:
        model = Task
        fields = ('taskName','followers','description','taskContractName','datetimeStart','datetimeEnd','status')

class DocumentGetSerializer(serializers.ModelSerializer):
    contract = serializers.StringRelatedField()
    class Meta:
        model = Document
        fields = ('documentName', 'description', 'file', 'contract')

class TaskPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('taskName','followers','description','taskContractName','datetimeStart','datetimeEnd','status')

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('documentName','description','file','contract')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
#######################################################################
def getCurrentUser(request):
    return request.user

def contractlink(request):
    return render(request, "tableofcontracts.html")

def tasklink(request):
    return render(request, "tableoftasks.html")

def taskaddlink(request):
    return render(request, "tasksPlus.html")

def contractDetailLink(request,pk):
    try:
        contract_id=Contract.objects.get(pk=pk)
        task = Task.objects.filter(taskContractName = pk)
    except Contract.DoesNotExist:
        raise Http404("Contract does not exist")
    return render(request, "contractTemplate.html",context = {'contractid':contract_id, 'tasks' : task})

def main(request):
    return render(request,'main.html')


#######################################################################
class CurrentUserView(generics.RetrieveAPIView):
    def get(self, request):
        userName = getCurrentUser(request)
        user = User.objects.get(username = userName)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    def get(self, request):
        # getCurrentUser(request)
        queryset = self.get_queryset()
        # template_name = 'tableofcontracts.html'
        users = User.objects.all()#filter(user = 'getCurrentUser(request)')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class ContractView(generics.ListAPIView):
    queryset = Contract.objects.all()
    def get(self, request):
        # getCurrentUser(request)
        queryset = self.get_queryset()
        # template_name = 'tableofcontracts.html'
        contracts = Contract.objects.all()#filter(user = 'getCurrentUser(request)')
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

class ContractDetailView(generics.RetrieveAPIView):
    def get_object(self, code):
        try:
            return Contract.objects.get(id = code)
        except:
            return Response(status=404)
    queryset = Contract.objects.all() #get(code = code)
    def get(self,request,code):
        contract = Contract.objects.get(id = code)
        queryset = self.get_queryset()
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

class TaskView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskGetSerializer
    def get(self, request):
        getCurrentUser(request)
        # getTasks()
        queryset = self.get_queryset()
        # template_name = 'tableofcontracts.html'
        tasks = Task.objects.all().order_by('taskContractName')#filter(user = 'getCurrentUser(request)')
        serializer = TaskGetSerializer(tasks, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = TaskPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class TaskUserFilteringView(generics.ListAPIView):
    def get_object(self, request):
        try:
            return Task.objects.filter(followers = getCurrentUser(request))
        except:
            return Response(status=404)
    queryset = Task.objects.all()
    def get(self,request):
        task = Task.objects.filter(followers = getCurrentUser(request))
        queryset = self.get_queryset()
        serializer = TaskGetSerializer(task, many=True)
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
        serializer = TaskGetSerializer(task, many=True)
        return Response(serializer.data)
<<<<<<< HEAD

class DocumentView(generics.ListAPIView):
    queryset = Document.objects.all()
    parser_classes = [MultiPartParser]
    def get(self, response):
        document = Document.objects.all()
        queryset = self.get_queryset()
        serializer = DocumentGetSerializer(document, many=True)
        return Response(serializer.data)
    def post(self,response):
        serializer = DocumentSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
# class DocumentsView(generics.ListAPIView):
#     queryset = Document.objects.filter(contract =  )
#     def get(self, request):
#         getCurrentUser(request)
#         queryset = self.get_queryset()
#         # template_name = 'tableofcontracts.html'
#         # documents = Document.objects.all()
#         serializer = ContractSerializer(queryset, many=True)
#         return Response(serializer.data)

#######################################################################

def getCurrentUser(request):
    return request.user

# def getTasks():
#     print(Task.objects.all())
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
=======
>>>>>>> e39e5baa650fe3f9cd4e3effa8862facca170388
