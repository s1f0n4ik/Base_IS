# urls.py
from django.urls import path
from .views import StudentListCreateView, EnrollmentStatsView

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list'),
    path('enrollment-stats/', EnrollmentStatsView.as_view(), name='enrollment-stats'),
]