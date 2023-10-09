from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('student/', StudentAPI.as_view()),
    #  path('', home),
    #  path('student/',post_student ),
    #  path('update-student/<id>/', update_student),
    #  path('delete-student/<id>/', delete_student),
     path('get-book/', get_book),
     path('register/', RegisterUser.as_view()),
     path('create-book/', NewBook.as_view()),
     path('book-assign/', get_books_assigned),
     path('new-book-assign/', AssignBook.as_view())
     #path('new-book-assign/',new_book_assign_to_student)
]