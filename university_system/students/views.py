# views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from django.db.models import Count
from datetime import datetime


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentStatsView(generics.GenericAPIView):
    def get(self, request):
        date_str = request.query_params.get('date', None)
        if not date_str:
            return Response({"error": "Date parameter is required"}, status=400)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        count = Student.objects.filter(enrollment_date=date).count()
        students = Student.objects.filter(enrollment_date=date)

        serializer = StudentSerializer(students, many=True)

        return Response({
            "date": date_str,
            "count": count,
            "students": serializer.data
        })