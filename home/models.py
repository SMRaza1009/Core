from django.db import models


# Create your models here.
class BookAssigned(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    no_of_days = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)
    fine = models.IntegerField(default=0)
    return_date = models.DateField(null=True, blank=True)

# apne check kara? 
# API to assign book to student, validate if book is already assigned then throw 400 else return successfully assigned
# API to update BookAssign when students comes to return the book, calculate fine as well



class Category(models.Model):
    category_name = models.CharField(max_length=100)
     

class Book(models.Model):
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=100) 
    def __str__(self):
        return self.book_title

      


class Student(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    father_name = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    