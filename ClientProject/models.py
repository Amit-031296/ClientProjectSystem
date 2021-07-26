from django.db import models
from django.contrib.auth.models import User

#Model Name = Client
class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    client_updated = models.DateTimeField(auto_now=True)
    client_created = models.DateTimeField(auto_now_add=True)
    client_created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="clients")

    def __str__(self):
        return self.first_name

#Model Name = Project
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_updated = models.DateTimeField(auto_now=True)
    project_created = models.DateTimeField(auto_now_add=True)
    project_client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name="project_client")
    project_users = models.ManyToManyField(User, blank=True,related_name="project_users")
    project_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.project_name


