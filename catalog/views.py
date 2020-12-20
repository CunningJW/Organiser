from django.shortcuts import render, redirect
from .models import Contract, Task, Document
from rest_framework import serializers, generics, mixins
# from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import User



from rest_framework.views import APIView

# Create your views here.
########################################################################

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id','contractName','zakupkiId','dateStart','dateEnd','display_tasks','getLink','linkToZakupkigov','currentUsers')



class TaskGetSerializer(serializers.ModelSerializer):
    taskContractName = serializers.StringRelatedField()
    followers = serializers.StringRelatedField()
    class Meta:
        model = Task
        fields = ('taskName','followers','description','taskContractName','datetimeStart','datetimeEnd','status')

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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tableofcontracts.html'
    queryset = Contract.objects.all()
    def get(self, request):
        # getCurrentUser(request)
        queryset = self.get_queryset()
        # template_name = 'tableofcontracts.html'
        contracts = Contract.objects.all()#filter(user = 'getCurrentUser(request)')
        serializer = ContractSerializer(contracts, many=True)
        return Response({'serializer': serializer,'contracts': contracts})

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


class TaskView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasksPlus.html'
    # serializer_class = TaskPostSerializer

    def get(self, request):
        getCurrentUser(request)

        contracts = Contract.objects.all()
        users = User.objects.all()

        serializer = TaskPostSerializer()
        return Response({'serializer': serializer,'contracts': contracts, 'users': users})

    def post(self, request):
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
            return Task.objects.filter(followers = getCurrentUser(request))
        except:
            return Response(status=404)
    queryset = Task.objects.all()
    def get(self,request):
        myTasks = Task.objects.filter(followers = getCurrentUser(request))
        queryset = self.get_queryset()
        serializer = TaskGetSerializer(myTasks, many=True)
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
        serializer = TaskGetSerializer(task, many=True)
        return Response(serializer.data)
