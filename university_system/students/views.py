# views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import Student, Faculty, Program
from .serializers import StudentSerializer, FacultySerializer, ProgramSerializer
from django.db.models import Count, Q
from datetime import datetime


class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()

        # Фильтрация по дате зачисления
        enrollment_date = self.request.query_params.get('enrollment_date', None)
        if enrollment_date:
            try:
                date = datetime.strptime(enrollment_date, '%Y-%m-%d').date()
                queryset = queryset.filter(enrollment_date=date)
            except ValueError:
                pass

        # Фильтрация по факультету
        faculty_id = self.request.query_params.get('faculty_id', None)
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)

        # Фильтрация по направлению
        program_id = self.request.query_params.get('program_id', None)
        if program_id:
            queryset = queryset.filter(program_id=program_id)

        # Фильтрация по курсу
        course = self.request.query_params.get('course', None)
        if course:
            queryset = queryset.filter(course=course)

        # Фильтрация по гражданству
        citizenship = self.request.query_params.get('citizenship', None)
        if citizenship:
            queryset = queryset.filter(citizenship__icontains=citizenship)

        # Фильтрация по периоду зачисления
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(enrollment_date__range=[start, end])
            except ValueError:
                pass

        return queryset.order_by('last_name', 'first_name')


class FacultyListView(generics.ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class ProgramListView(generics.ListAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        faculty_id = self.request.query_params.get('faculty_id', None)
        if faculty_id:
            return Program.objects.filter(faculty_id=faculty_id)
        return Program.objects.all()