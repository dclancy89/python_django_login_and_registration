from __future__ import unicode_literals

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.db import models

# Create your models here.

class UserManager(models.Manager):
	def validate_user(request, postData):
		errors = {}

		# validate first name field
		if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
			if len(postData['first_name']) < 2:
				errors['first_name_length'] = "First Name must be 2 or more characters."
			if not postData['first_name'].isalpha():
				errors['first_name_alpha'] = "First Name can only container letters."

		# validate last name field
		if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
			if len(postData['first_name']) < 2:
				errors['last_name_length'] = "Last Name must be 2 or more characters."
			if not postData['first_name'].isalpha():
				errors['last_name_alpha'] = "Last Name can only container letters."

		# validate email
		try:
			validate_email(postData['email'])
		except ValidationError:
			errors['email'] = "This is not a valid email."
		else:

			if User.objects.filter(email=postData['email']):
				errors['email'] = "This user already exists."



		# validate password
		if len(postData['password']) < 8:
			errors['password'] = "Password must be at least 8 characters long"

		# check if passwords match
		if postData['password'] != postData['confirm_pw']:
			errors['confirm_pw'] = "Passwords must match"


		return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

	objects = UserManager()




