from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        Users.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        user = Users.objects.filter(email = request.POST['email'])
        request.session['userid'] = user[0].id
        request.session['name'] = user[0].first_name
        context = {
            'user':user[0]
        }
        return render(request, 'success.html',context)
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = Users.objects.validate_login(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        user = Users.objects.filter(email = request.POST['email'])
        request.session['userid'] = user[0].id
        request.session['name'] = user[0].first_name
        return redirect('/success')
    return redirect('/')

def all_books(request):
    if "userid" not in request.session:
        return redirect('/')
    else:
        context = {
            'user':Users.objects.get(id=request.session['userid']),
            'all_books': Books.objects.all()

        }
        return render(request, "success.html", context)

def add_book(request):
    if request.method == "POST":
        errors = Books.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/success')
        user = Users.objects.get(id=request.session["userid"])
        book = Books.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            uploaded_by = user
        )
        user.liked_books.add(book)
        return redirect(f'/books/{book.id}')
    return redirect('/success')

def book(request, book_id):

    context = {
        'book': Books.objects.get(id=book_id),
        'current_user': Users.objects.get(id=request.session['userid']),
    }
    return render(request,"book.html", context)

def edit_book(request, book_id):
    book = Books.objects.get(id=book_id)
    book.description = request.POST['description']
    book.save()
    return redirect(f'/books/{book.id}')

def delete_book(request, book_id):
    c = Books.objects.get(id=book_id)
    c.delete()
    return redirect('/success')

def like(request, book_id):
    user = Users.objects.get(id=request.session['userid'])
    book = Books.objects.get(id=book_id)
    user.liked_books.add(book)
    return redirect(f'/books/{book.id}')

def unlike(request, book_id):
    user = Users.objects.get(id=request.session['userid'])
    book = Books.objects.get(id=book_id)
    user.liked_books.remove(book)
    return redirect(f'/books/{book.id}')

def logout(request):
    request.session.flush()
    return redirect('/')

    





