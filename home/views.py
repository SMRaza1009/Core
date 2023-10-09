from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Book
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken





# Create your views here.

# API to assign book to student, validate if book is already assigned then throw 400 else return successfully assigned -- completed!
# API to update BookAssign when students comes to return the book, calculate fine as well -- not completed!


# bhai main phele serializers se hi karne ki koshish mai laga hua tha abhi just for understanding ke liye is tarah kar raha tha magar serialize
# r

#  chalo karo jaldi phr test karte hain, aj proper functionality chalni chahiye hai

        

# asal yeh likha tha yeh chal raha hai! magar sara masla views ka hai!
class AssignBook(APIView):
    def post(self, request):
        data = request.data
        serializers = BookAssignedCreateSerializer(data=data)
        # test karo thunder client se bhai -- ok
        try:
            serializers.is_valid()
            serializers.save()
            return Response({'status': 200, 'message': 'Book assigned successfully'})
        except Exception as e:
            return Response({'status': 400, 'message': str(e)})
            


@api_view(['GET'])
def get_book(request):
    queryset = Book.objects.all()
    print(queryset)
    serializers = BookSerializer(queryset, many = True)
    return Response({'status': 200, 'payload' : serializers.data})


@api_view(['GET'])
def get_books_assigned(request):
    queryset = BookAssigned.objects.all()
    serializers = BookAssignedSerializer(queryset, many = True)
    return Response({'status': 200, 'payload' : serializers.data, 'message': 'Book assigned successfully!'})

class NewBook(APIView):
    def post(self, request):
        serializers = BookSerializer(data = request.data)
        if not serializers.is_valid():
            print(serializers.errors)
            return Response({'status':403, 'errors': serializers.errors, 'message': 'Something went wrong!'})
        serializers.save()
        
        return Response({'status':200, 'payload' : serializers.data , 'message': 'your data has been saved!'})


class RegisterUser(APIView):
    
    def post(self, request):
        serializers = UserSerializer(data = request.data)
        
        if not serializers.is_valid():
            print(serializers.errors)
            return Response({'status':403, 'errors': serializers.errors, 'message': 'Something went wrong!'})
        serializers.save()
        
        user = User.objects.get(username = serializers.data['username'])
        refresh = RefreshToken.for_user(user)
        #token_obj, _ = Token.objects.get_or_create(user=user) # without JWT token manually
        
        return Response({'status':200, 'payload' : serializers.data,'refresh': str(refresh), 'access': str(refresh.access_token), 'message': 'your data has been saved!'})


class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Student.objects.all()
        serializers = StudentSerializer(queryset, many = True)
        print(request.user)
        return Response({'status': 200, 'payload' : serializers.data})
    
    def post(self, request):
        data = request.data
        serializers = StudentSerializer(data = request.data)
    
    
        if not serializers.is_valid():
            print(serializers.errors)
            return Response({'status': 403, 'errors': serializers.errors, 'message': 'Something went wrong!' })
    
        serializers.save()
        return Response({'status': 200, 'payload' : serializers.data, 'message' : 'you sent' })

    
    def put(self, request):
        pass
    
    def patch(self, request):
        try:
            queryset = Student.objects.get(id = request.data['id'])
            serializers = StudentSerializer(queryset , data = request.data , partial = True) # here partial true (PATCH METHOD) ka matlab hai ke humey update kartey time sari fields dene ki zaroorat nai parhe gi bas jo field update karni hai wohi deni hogi.add()
        
            if not serializers.is_valid():
                print(serializers.errors)
                return Response({'status': 403, 'errors': serializers.errors, 'message': 'Something went wrong!' })
        
            serializers.save()
        
            return Response({'status': 200, 'payload' : serializers.data, 'message' : 'Your data is updated!' })
    
        except Exception as e:
            return Response ({'status': 403, 'message' : 'invalid id enter!'})
    
    def delete(self, request):
        try:
            id = request.GET.get('id')
            queryset = Student.objects.get(id = id)
            queryset.delete()
        
            return Response({'status':200, 'message': 'deleted'})
    
        except Exception as e:
            print(e)
            return Response({'status':403, 'message' : 'invalid id'})














# @api_view(['GET'])
# def home(request):
#     queryset = Student.objects.all()
#     serializers = StudentSerializer(queryset, many=True)
#     return Response({'status': 200, 'payload': serializers.data}) 



# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     serializers = StudentSerializer(data = request.data)
    
    
#     if not serializers.is_valid():
#         print(serializers.errors)
#         return Response({'status': 403, 'errors': serializers.errors, 'message': 'Something went wrong!' })
    
#     serializers.save()
        
        
#     return Response({'status': 200, 'payload' : serializers.data, 'message' : 'you sent' })


# @api_view(['PUT'])
# def update_student(request, id):
    # try:
    #     queryset = Student.objects.get(id = id)
    #     serializers = StudentSerializer(queryset , data = request.data , partial = True) # here partial true (PATCH METHOD) ka matlab hai ke humey update kartey time sari fields dene ki zaroorat nai parhe gi bas jo field update karni hai wohi deni hogi.add()
        
    #     if not serializers.is_valid():
    #         print(serializers.errors)
    #         return Response({'status': 403, 'errors': serializers.errors, 'message': 'Something went wrong!' })
        
    #     serializers.save()
        
    #     return Response({'status': 200, 'payload' : serializers.data, 'message' : 'you sent' })
    
    # except Exception as e:
    #     return Response ({'status': 403, 'message' : 'invalid id enter!'})
    
# @api_view(['DELETE'])
# def delete_student(request, id):
    # try:
    #     queryset = Student.objects.get(id = id)
    #     queryset.delete()
        
    #     return Response({'status':200, 'message': 'deleted'})
    
    # except Exception as e:
    #     print(e)
    #     return Response({'status':403, 'message' : 'invalid id'})
    
# http://127.0.0.1:8000/delete-student/?id=7
# @api_view(['DELETE'])
# def delete_student(request):
#     try:
#         id = request.GET.get('id')
#         queryset = Student.objects.get(id = id)
#         queryset.delete()
        
#         return Response({'status':200, 'message': 'deleted'})
    
#     except Exception as e:
#         print(e)
#         return Response({'status':403, 'message' : 'invalid id'})    
            
    
