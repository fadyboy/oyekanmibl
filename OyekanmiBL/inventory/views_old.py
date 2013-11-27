# Create your views here.
#from django.http import HttpResponse
from django.shortcuts import render_to_response
# import django inbuilt module for authentication
from django.contrib.auth import authenticate, login, logout
# add import to take care of crsf validation errors
#from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# Create a view for the Home page

def home(request):
	''' Home page takes the username and password entries which are authenticated 
	which enables the user to log on to website'''
	
	message = '' 
	username = password = "" # set username and password to empty string
			
	return render_to_response("inventory/home.html", {'message': message, 'username': username}, context_instance=RequestContext(request))
	#return httpResponse("Oyekanmi")
	
# Create a view for the logged in user page

def mylogin(request):
	#username = request.POST.get('username')
	message = "Please login below.."
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				message = "Login successful: %s" % user
				
				return render_to_response("inventory/login.html", {'message': message}) # pass in username to message
				
			else:
				message = "Your account is not active"
				
		else:
			message = "Your login details are not correct"
			
	return render_to_response("inventory/home.html", {'message': message})
	
		
# Create a view for the Add Product page

@login_required
def addproduct(request):
	return render_to_response("inventory/addproduct.html", {'message': "Add new products here"})
	

# Create a view for the Add Category page

def addcategory(request):
	return render_to_response("inventory/addcategory.html", {'message': "Add new category here"})
	

# Create a view for Receive product page

def receiveproduct(request):
	return render_to_response("inventory/receiveproduct.html", {'message': "Receive products here"})
	

# Create a view for the Issue product page

def issueproduct(request):
	return render_to_response("inventory/issueproduct.html", {'message': "Issue products here"})
	
@login_required	
def mylogout(request):
	
	logout(request)
	
	return render_to_response("inventory/mylogout.html", {'message': "You are now logged out"})




	
	
	

