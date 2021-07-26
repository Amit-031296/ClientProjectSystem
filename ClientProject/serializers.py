from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from ClientProject.models import Client,Project

import os
from django.conf import settings


class ClientSerializer(serializers.ModelSerializer):
    
    #Serializer method for client name
    client_name = serializers.SerializerMethodField('get_fullname')
    class Meta:
        model = Client
        fields = ['id', 'client_name','client_created_by','client_created']

    def get_fullname(self,client):
        fullname = "{} {}".format(client.first_name,client.last_name)
        return fullname

class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name','client_created_by']
    
    def save(self):
        try:
            print(self.validated_data)
            first_name = self.validated_data['first_name']
            last_name = self.validated_data['last_name']
            created_by = self.validated_data['client_created_by']
            client = Client(
								first_name=first_name,
								last_name=last_name,
								client_created_by=created_by
								)
            client.save()
            return client
        except KeyError:
            raise serializers.ValidationError({"response": "client must have first name and last name"})

class ClientProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField('get_fullname')
    
    class Meta:
        model = Client
        fields = ['pk', 'client_name','client_created','client_created_by','client_updated']
        
    def get_fullname(self,client):
        fullname = "{} {}".format(client.first_name,client.last_name)
        return fullname

class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'first_name','last_name']
    
class ProjectSerializer(serializers.ModelSerializer):
    get_username = serializers.SerializerMethodField('get_username_created_project')
    
    class Meta:
        model = Project
        fields = ['pk','project_name','project_created','get_username']

    def get_username_created_project(self,project):
        username = project.project_created_by.username
        return username

#Register Serializer
class RegistrationSerializer(serializers.ModelSerializer):

    password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username','password', 'password2']
        extra_kwargs = {
				'password': {'write_only': True},
		}	


    def	save(self):
        user = User(
					username=self.validated_data['username']
				)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user