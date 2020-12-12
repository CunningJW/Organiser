from django.shortcuts import render
from rest_framework import serializers, generics
# from rest_framework.decorators import api_view

from rest_framework.views import APIView

from rest_framework.response import Response
from django.shortcuts import render

##########!Models!#########
from .models import Contract, Task, Document
###########################




class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('contractName','zakupkiId','dateStart','dateEnd','display_tasks','get_absolute_url')

class TaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task ('taskName','description','contract','datetimeStart','datetimeEnd','status')

class ContractView(generics.ListAPIView):
    def get(self, request):
        template_name = 'contract_list.html'
        contracts = Contract.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = ContractSerializer(contracts, many=True)
        return Response({"contracts": serializer.data})





def client(request):
    return render(request, "tableofcontracts.html")
#
# @api_view(['GET','POST'])
# def list_contract_names(request):
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
#
# # @api_view(['GET','DELETE','PUT'])
# # def contract_details(request, code):
# #     try:
# #         contract = Contract.objects.get(code=code)
# #     except:
# #         return Response(status=404)
# #
# #     if request.method == 'GET':
# #         serializer = ContractSerializer(course)
# #         return Response(serializer.data)
# #     elif request.method == 'PUT':    # Update
# #         serializer = ContractSerializer(contract, data=request.data)
# #         if serializer.is_valid():
# #            serializer.save()    # Update table in DB
# #            return Response(serializer.data)
# #
# #         return Response(serializer.errors, status=400)  # Bad request
# #     elif request.method == 'DELETE':
# #         contract.delete()
# #         return Response(status=204)
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
#
#
def main(request):
    return render(
        request,
        'main.html',
    )
