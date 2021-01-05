from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from .serializers import *


#####=====================================####
                #####REST###
#####=====================================####


class ContractViewRest(APIView):
    queryset = Contract.objects.all()
    def get(self, request):
        queryset = Contract.objects.all()
        serializer = ContractSerializer(queryset, many=True)
        return Response(serializer.data)

class TaskUserViewRest(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskPostSerializer
    def get(self,request):
        queryset = Task.objects.all()
        serializer = TaskListSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = TaskPostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class DocumentViewRest(APIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser]

    def get(self, request):
        queryset = Document.objects.all()
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print("err")
            return Response(serializer.errors)
