from django.urls import path
from ClientProject.views import(
	ApiClientListView,
    api_create_client_view,
	LoginView,
	api_client_info,
	api_client_update_view,
	api_client_delete_view,
	client_project_create,
	project_assigned_log_user,
	registration_view,
	logout_view
)

app_name = 'ClientProject'

urlpatterns = [

	#Retrieve info of a client along with projects assigned to its users
	path('clients/<pk>/', api_client_info, name="api_client_info"),

	#Update info of a client
	path('clients/update/<pk>', api_client_update_view, name="api_client_update_view"),

	#Delete a client
	path('clients/delete/<pk>', api_client_delete_view, name="api_client_delete_view"),

	

	#List of All client url
	path('list', ApiClientListView.as_view(), name="list"),

	#Create a new client
	path('create', api_create_client_view, name="create"),
	
	#Create a new project
	path('clients/<pk>/projects/',client_project_create,name="client_project_create"),

	#List of all projects assigned to the logged-in user
	path('users/projects/',project_assigned_log_user,name="project_assigned_log_user"),

	# Login,Register and Logout
	#login url
	path('login',LoginView.as_view(),name="login"),

	#Register url
	path('register', registration_view, name="register"),

	#Logout url
	path('logout',logout_view,name="logout_view")
	
]