from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *

# Create your views here.
def index(request):
	if request.session.get('id') != None:
		return redirect('/success')

	return render(request, 'users/index.html')

def register(request):
	errors = User.objects.validate_user(request.POST)

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
		return redirect('/')
	else:
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password']
		hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_pw)
		user = User.objects.get(email=email)
		request.session['id'] = user.id

		messages.success(request, 'Successfully Registered')
		return redirect('/success')

def login(request):
	email = request.POST['email']
	password = request.POST['password']

	# check if the user exists
	user = User.objects.filter(email=email)
	if len(user) > 0:
		# if it does, check password
		isPassword = bcrypt.checkpw(password.encode(), user[0].password.encode())
		if isPassword:
			request.session['id'] = user[0].id
			messages.success(request, 'Successfully Logged In')
			return redirect('/success')
		else:
			# wrong password
			messages.error(request, "Incorrect username/password combination.")
			return redirect('/')
	else:
		# user doesn't exists
		messages.error(request, "User does not exists")
		return redirect('/')



def success(request):
	# check if a user is logged in
	if request.session.get('id') == None:
		return redirect('/')

	user = User.objects.get(id=request.session['id'])
	context = {'user': user}
	return render(request, 'users/success.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')


