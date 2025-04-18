# urls.py
from django.urls import path
from .views import StudentListView, FacultyListView, ProgramListView

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('faculties/', FacultyListView.as_view(), name='faculty-list'),
    path('programs/', ProgramListView.as_view(), name='program-list'),
]
