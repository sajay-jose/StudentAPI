from .views import *
from django.urls import path

urlpatterns = [
    path('register/student/',StudentRegister.as_view(), name="studentregister"),
    path('login/',UserLogin.as_view(), name="login"),
    path('studentdetails/',StudentDetail.as_view(), name="studentdetails"),
    path('search/student/',UserSearchView.as_view(), name="searchstudent")
]