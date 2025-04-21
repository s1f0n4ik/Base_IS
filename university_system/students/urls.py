# urls.py
from django.urls import path
from .views import StudentListView, DepartmentListView, ProgramListView

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('departments/', DepartmentListView.as_view(), name='faculty-list'),
    path('programs/', ProgramListView.as_view(), name='program-list'),
]
