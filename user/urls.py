from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.all_books),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('books/<int:book_id>', views.book),
    path('books/<int:book_id>/edit', views.edit_book),
    path('books/<int:book_id>/delete', views.delete_book),
    path('like/<int:book_id>', views.like),
    path('unlike/<int:book_id>', views.unlike),

]