from django.db import models
import re
import bcrypt

# Create your models here.
class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters long. "

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        
        user = Users.objects.filter(email=postData['email'])
        if len(user) > 0:
            errors['double'] = "User with email address already exists."

        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        return errors

    def validate_login(self, postData):
        errors={}
        user = Users.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email not entered."
        if len(postData['password']) < 8:
            errors['password'] = "Password not entered correctly."
        elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match."
        return errors
        
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class BooksManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title is required."
        if len(postData['description']) < 5:
            errors['description'] = "Description much be at least 5 characters."
        return errors

class Books(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(Users, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(Users, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BooksManager()

