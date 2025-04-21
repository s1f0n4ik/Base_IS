from rest_framework import generics
from .models import Student, Department, Program
from .serializers import StudentSerializer, DepartmentSerializer, ProgramSerializer
from django.db.models import Q
from datetime import datetime


class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()
        params = self.request.query_params

        # Фильтрация по датам
        if 'enrollment_date' in params:
            try:
                date = datetime.strptime(params['enrollment_date'], '%Y-%m-%d').date()
                queryset = queryset.filter(enrollment_date=date)
            except ValueError:
                pass

        if 'start_date' in params and 'end_date' in params:
            try:
                start = datetime.strptime(params['start_date'], '%Y-%m-%d').date()
                end = datetime.strptime(params['end_date'], '%Y-%m-%d').date()
                queryset = queryset.filter(enrollment_date__range=[start, end])
            except ValueError:
                pass

        # Множественная фильтрация по кафедрам
        if 'departments' in params:
            departments = params['departments'].split(',')
            queryset = queryset.filter(department_id__in=departments)

        # Множественная фильтрация по направлениям
        if 'programs' in params:
            programs = params['programs'].split(',')
            queryset = queryset.filter(program_id__in=programs)

        # Множественная фильтрация по курсам
        if 'courses' in params:
            courses = params['courses'].split(',')
            queryset = queryset.filter(course__in=courses)

        # Фильтрация по гражданству
        if 'citizenship' in params:
            queryset = queryset.filter(citizenship__icontains=params['citizenship'])

        # Фильтрация по типу обучения (бюджет/контракт)
        if 'education_types' in params:
            types = params['education_types'].split(',')
            queryset = queryset.filter(education_type__in=types)

        # Фильтрация по основанию поступления (целевое/квота/общий)
        if 'admission_bases' in params:
            bases = params['admission_bases'].split(',')
            queryset = queryset.filter(admission_basis__in=bases)

        return queryset.order_by('last_name', 'first_name')


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgramListView(generics.ListAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id', None)
        if department_id:
            return Program.objects.filter(department_id=department_id)
        return Program.objects.all()