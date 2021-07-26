from inspect import cleandoc
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from ClientProject.models import Client, Project
from rest_framework import serializers
from ClientProject.serializers import(
    ClientSerializer,
    ClientCreateSerializer,
    ClientProjectSerializer,
    ClientUpdateSerializer,
    ProjectSerializer,
    RegistrationSerializer)
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.contrib.auth.models import User
import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate,logout
from django.shortcuts import render,redirect



'''
List of all clients View
URL: http://127.0.0.1:8001/api/list

#Input - Basicauth
Request - Get


OutPut - 
[
    {
        "id": 1,
        "client_name": "client1 system",
        "client_created_by": 2,
        "client_created": "2021-07-24T13:33:49.243592Z"
    },
    {
        "id": 2,
        "client_name": "client2 system",
        "client_created_by": 3,
        "client_created": "2021-07-24T13:34:01.402430Z"
    },
    {
        "id": 3,
        "client_name": "client3 system",
        "client_created_by": 2,
        "client_created": "2021-07-24T13:34:13.842265Z"
    },
    {
        "id": 4,
        "client_name": "client4 system",
        "client_created_by": 3,
        "client_created": "2021-07-24T13:34:30.323108Z"
    }
]
'''
class ApiClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    

'''
Create a new client
URL: http://127.0.0.1:8001/api/create

#Input - Basicauth
Request - POST
form-data:
first_name - client5
last_name - system
client_created_by - 2(pk value)


OutPut - 
{
    "response": "created",
    "id": 5,
    "client_name": "client5 system",
    "client_created_at": "2021-07-25T12:24:25.872525Z",
    "client_created_by": "testuser1"
}
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_client_view(request):
    if request.method == 'POST':
        data = request.data
        print(request.user)
        serializer = ClientCreateSerializer(data=data)
        if serializer.is_valid():
            client = serializer.save()
            data = {}
            data["response"] = "created"
            data['id'] = client.pk
            fullname = "{} {}".format(client.first_name,client.last_name)
            data['client_name'] = fullname
            data['client_created_at'] = client.client_created
            data['client_created_by'] = client.client_created_by.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   



'''
Retrieve info of a client along with projects assigned to its users
URL: http://127.0.0.1:8001/api/clients/<pk>/ 

#Input - Basicauth
Request - GET



OutPut - 
{
    "pk": 1,
    "client_name": "client1 system",
    "client_created": "2021-07-24T13:33:49.243592Z",
    "client_created_by": 2,
    "client_updated": "2021-07-24T13:33:49.243592Z",
    "projects": [
        {
            "id": 1,
            "name": "project1"
        }
    ]
}
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_client_info(request,pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientProjectSerializer(client)
        data = serializer.data
        projects = list()
        a = Client.objects.get(pk=client.pk)
        b = a.project_client.all()
        if len(b) == 0:
            projects = []
        else:
            for i in b:
                dict1 = dict()
                dict1['id'] = i.pk
                dict1['name'] = i.project_name
                projects.append(dict1)
        data['projects'] = projects
        return Response(data)

'''
Login View
URL: http://127.0.0.1:8001/api/login

#Input - form-data
username - testuser1
password - ########

OutPut - 
{
    "response": "Successfully authenticated.",
    "pk": 2,
    "username": "testuser1"
}
'''
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(username=username, password=password)
        if account:
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['username'] = account.username
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'
            
        return Response(context)

'''
Update info of a client
URL: http://127.0.0.1:8001/api/clients/update/<pk>

#Input - form-data
first_name - client1updated
last_name - system

OutPut - 
{
    "response": "CLIENT UPDATED",
    "id": 1,
    "client_name": "client1updated system",
    "client_created_at": "2021-07-24T13:33:49.243592Z",
    "client_created_by": "testuser1",
    "client_updated_at": "2021-07-25T12:35:50.596439Z"
}
'''
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_client_update_view(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    user = request.user
    if client.client_created_by == user:
        if request.method == 'PUT':
            serializer = ClientUpdateSerializer(client, data=request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['response'] = "CLIENT UPDATED"
                data['id'] = client.pk
                fullname = "{} {}".format(client.first_name,client.last_name)
                data['client_name'] = fullname
                data['client_created_at'] = client.client_created
                data['client_created_by'] = client.client_created_by.username
                data['client_updated_at'] = client.client_updated
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'response':"You don't have permission to edit that."})


'''
Delete a client
URL: http://127.0.0.1:8001/api/clients/delete/<pk>

#Input - Basicauth
Request - DELETE

OutPut - 
{
    "response": "CLIENT DELETED"
}
'''
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_client_delete_view(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    user = request.user
    if client.client_created_by == user:
        if request.method == 'DELETE':
            operation = client.delete()
            data = {}
            if operation:
                data['response'] = "CLIENT DELETED"
            return Response(data=data)
    else:
        return Response({'response':"You don't have permission to delete that."})    


'''
Create a new project
URL: http://127.0.0.1:8001/api/clients/<pk>/projects/

#Input - Basicauth
Request - POST

raw json
{
    "project_name":"project66",
    "users" : [
    		{
                "id" : 2,
                "name" : "testuser1"
    		}
	]
}

OutPut - 
{
    "id": 16,
    "project_name": "project66",
    "project_client": "client4 system",
    "users": [
        {
            "id": 2,
            "name": "testuser1"
        }
    ],
    "project_created": "2021-07-25T12:48:37.238140Z",
    "project_created_by": "testuser1"
}
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def client_project_create(request,pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        data = request.data
        project = Project(project_name=data['project_name'],project_client=client,project_created_by=request.user)
        project.save()
        users = data['users']
        users_id = list()
        for i in users:
            users_id.append(i['id'])
        user_objects = User.objects.filter(id__in=users_id)   
        for i in user_objects:
            project.project_users.add(i)
        project.save()
        a = project.project_users.all()
        project_users_list = list()
        for i in a:
            project_users_list.append({'id':i.pk,'name':i.username})
        data1 = dict()
        data1['id'] = project.pk
        data1['project_name'] = project.project_name
        fullname = "{} {}".format(project.project_client.first_name,project.project_client.last_name)
        data1['project_client'] = fullname
        data1['users'] = project_users_list
        data1['project_created'] = project.project_created
        data1['project_created_by'] = project.project_created_by.username
        return Response(data1)


'''
List of all projects assigned to the logged-in user
URL: http://127.0.0.1:8001/api/users/projects/

#Input - Basicauth
Request - GET

OutPut - 
[
    {
        "pk": 14,
        "project_name": "project 9",
        "project_created": "2021-07-24T14:15:31.960561Z",
        "get_username": "testuser1"
    },
    {
        "pk": 15,
        "project_name": "project 10",
        "project_created": "2021-07-25T04:45:38.260530Z",
        "get_username": "testuser1"
    }
]
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_assigned_log_user(request):
    if request.method == 'GET':
        data = Project.objects.filter(project_users__username=request.user.username)
        serializer = ProjectSerializer(data,many=True)
        data1 = serializer.data
        return Response(data1)


'''
Register View
URL: http://127.0.0.1:8001/api/register

#Input - form-data
username - testuser5
password - ########
password2 - ########

OutPut - 
{
    "response": "successfully registered new user.",
    "username": "testuser5",
    "pk": 6
}
'''
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        data_request = {}
        username = request.data.get('username').lower()
        if validate_username(username) != None:
            data['error_message'] = 'That username is already in use.'
            data['response'] = 'Error'
            return Response(data)
            
        password = request.data.get('password', '0')
        password2 = request.data.get('password2', '0')
        
        if password2!=password:
            data['response'] = "password must match"
            return Response(data)
            
        data_request['username'] = username
        data_request['password'] = password
        data_request['password2'] = password2
        print("data_request ==>",data_request)
        serializer = RegistrationSerializer(data=data_request)
		
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['username'] = user.username
            data['pk'] = user.pk
        else:
            data = serializer.errors
        return Response(data)

def validate_username(username):
    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    if user != None:
        return user

'''
Logout View
URL: http://127.0.0.1:8001/api/logout
'''
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return Response({'response':"user logout"})
