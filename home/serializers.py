from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
import datetime


# API to assign book to student, validate if book is already assigned then throw 400 else return successfully assigned
# API to update BookAssign when students comes to return the book, calculate fine as well

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        #fields = ['name', 'age', 'father_name', 'university_name', 'course_name']
        fields = "__all__" # include all fields at onces and do serialize
        # suppose if we dont't want to serialize 'age', so we use exclude command
        #exclude = ['age',]
    def validate(self, data):
        if 'age' in data and data['age'] < 18:
        #if data['age'] < 18:
            raise serializers.ValidationError({'error':'Age cannot be less than 18. '})
        
        if 'name' in data:
        #if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({'error':'Name must be string not an number.'})    
        return data
    
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        
   # Now, when our user are register, the password is not hashed we need to hashed user's password and
   # For hashing user password
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user    
        
    
    
    

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name',]            
        
        
class BookSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()
    class Meta:
        model = Book
        fields = '__all__'
        #depth = 1        # Depth will not work for specific given such as  fields = ['category_name',]
        
class BookAssignedSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    expected_return_date = serializers.SerializerMethodField()
    
    def get_expected_return_date(self,obj):
        return obj.created_at + datetime.timedelta(days=obj.no_of_days)
         
    class Meta:
        model = BookAssigned
        fields = "__all__"
        
class BookAssignedCreateSerializer(serializers.ModelSerializer):         
    
    def validate(self, data):
        assigned = BookAssigned.objects.filter(book_id=data["book"], return_date__isnull=True).exists()
        if assigned:
            raise serializers.ValidationError("Book is already Assigned")
        return data

    class Meta:
        model = BookAssigned
        fields = "__all__"


            
           
