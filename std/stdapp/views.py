from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import *
import jwt
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import PersonalSerializer, CollegeSerializer, CourseSerializer, WorkExperienceSerializer,UserSerializer
# Create your views here.

def studentlogin(data):
    user = User(
        username = data['username'],
        password = make_password(data['password'])
    )
    user.save()
    return user

class StudentRegister(APIView):
    def post(self,request,format=None):
        try:
            student = request.data.get('student')
            print(student)
            Data = request.data.get('data')
            print(Data)
            stdlog = studentlogin(student)
            print(stdlog)
            student_data = Personal.objects.create(
                user_id = stdlog,
                Name = Data['name'],
                Gender = Data['Gender'],
                DOB = Data['DOB'],
                Contact_no = Data['Contact_no'],
                Whatsapp_no = Data['Whatsapp_no'],
                Qualification = Data['Qualification']  
            )
            student_data.save()

            college_data = College.objects.create(
                user_id = stdlog,
                college = Data['college']
                
            )

            college_data.save()

            course_data = Course.objects.create(
                user_id = stdlog,
                course = Data['course']
            )
            course_data.save()

            WorkExperiancedata = WorkExperiance.objects.create(
                user_id = stdlog,
                company = Data['company'],
                role = Data['role']
            )
            WorkExperiancedata.save()

            data = {"status":1}
            return JsonResponse(data, safe=False)
        except Exception as e:
            data = {"status":0}
            print(e)
            return JsonResponse(data, safe=False,status=400)


class UserLogin(APIView):
    def post(self,request,format=None):
        try:
            user = authenticate(request, username = request.data['username'], password = request.data['password'])
            if user is not None:
                userdata = User.objects.get(username=request.data['username'])
                login(request,user)
                data = {"token":[], "status":[]}
                each_item = {}
                each_item["token"] = jwt.encode({"username":userdata.username},"secret",algorithm="HS256")
                data["token"].append(each_item)
                each_item = {}
                each_item["status"]=1
                data["status"].append(each_item)
                return JsonResponse(data,safe=False)
            else:
                data = []
                each_item = {}
                each_item["status"] = 0
                data.append(each_item) 
        
        except Exception as e:
            print(e)
            data = []
            each_item = {}
            each_item["status"] = 0
            data.append(each_item)
            return JsonResponse(data,safe=False)





class StudentDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            user = request.user

            userdata = User.objects.get(id=user.id)
            user_serializer = UserSerializer(userdata)

            if userdata.is_superuser:
                data = {
                    'user': user_serializer.data,
                }
            else:
                personal = Personal.objects.get(user_id=user)
                personal_serializer = PersonalSerializer(personal)

                college = College.objects.filter(user_id=user)
                college_serializer = CollegeSerializer(college, many=True)

                course = Course.objects.filter(user_id=user)
                course_serializer = CourseSerializer(course, many=True)

                work_experience = WorkExperiance.objects.filter(user_id=user)
                work_experience_serializer = WorkExperienceSerializer(work_experience, many=True)

                data = {
                    'user': user_serializer.data,
                    'personal': personal_serializer.data,
                    'college': college_serializer.data,
                    'course': course_serializer.data,
                    'work_experience': work_experience_serializer.data,
                }
            return Response(data, status=200)
        except Personal.DoesNotExist:
            return Response({"error": "User details not found"}, status=404)

class UserSearchView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            query_params = request.query_params
            filters = Q()

            if 'enquiry_no' in query_params:
                filters &= Q(enquiry_no=query_params['enquiry_no'])
            if 'name' in query_params:
                filters &= Q(Name__icontains=query_params['name'])
            if 'gender' in query_params:
                filters &= Q(Gender=query_params['gender'])
            if 'qualification' in query_params:
                filters &= Q(Qualification=query_params['qualification'])
            if 'college' in query_params:
                filters &= Q(user_id__in=College.objects.filter(college__icontains=query_params['college']).values_list('user_id', flat=True))
            if 'contact_number' in query_params:
                filters &= Q(Contact_no=query_params['contact_number'])
            if 'whatsapp_number' in query_params:
                filters &= Q(Whatsapp_no=query_params['whatsapp_number'])
            if 'dob' in query_params:
                filters &= Q(DOB=query_params['dob'])
            if 'work_experience' in query_params:
                filters &= Q(user_id__in=WorkExperience.objects.filter(company__icontains=query_params['work_experience']).values_list('user_id', flat=True))

            personals = Personal.objects.filter(filters).distinct()
            data = []

            for personal in personals:
                colleges = College.objects.filter(user_id=personal.user_id)
                college_serializer = CollegeSerializer(colleges, many=True)
                
                courses = Course.objects.filter(user_id=personal.user_id)
                course_serializer = CourseSerializer(courses, many=True)
                
                work_experiences = WorkExperiance.objects.filter(user_id=personal.user_id)
                work_experience_serializer = WorkExperienceSerializer(work_experiences, many=True)
                
                user_data = {
                    'personal': PersonalSerializer(personal).data,
                    'college': college_serializer.data,
                    'course': course_serializer.data,
                    'work_experience': work_experience_serializer.data,
                }
                data.append(user_data)

            return Response(data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)