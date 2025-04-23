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

        # Основной фильтр для статусов (кроме отчисленных)
        status_filter = Q()
        # Фильтр для отчисленных
        expelled_filter = Q()

        # 1. Обработка статусов
        if 'statuses' in params:
            statuses = params['statuses'].split(',')

            # Разделяем статусы на обычные и отчисленных
            regular_statuses = [s for s in statuses if s != 'expelled']
            has_expelled = 'expelled' in statuses

            # Фильтр для обычных статусов
            if regular_statuses:
                status_filter &= Q(status__in=regular_statuses)

            # 2. Фильтр для отчисленных (без причин)
            if has_expelled and 'expulsion_reasons' not in params:
                expelled_filter = Q(status='expelled')

        # 3. Обработка причин отчисления
        if 'expulsion_reasons' in params:
            reasons = params['expulsion_reasons'].split(',')
            expelled_filter = Q(status='expelled', expulsion_reason__in=reasons)

        # 4-5. Комбинируем фильтры
        if status_filter and expelled_filter:
            main_filter = status_filter | expelled_filter
        elif status_filter:
            main_filter = status_filter
        else:
            main_filter = expelled_filter

        # Применяем дополнительные фильтры
        # Фильтрация по датам
        if 'enrollment_date' in params:
            try:
                date = datetime.strptime(params['enrollment_date'], '%Y-%m-%d').date()
                main_filter &= Q(enrollment_date=date)
            except ValueError:
                pass

        if 'start_date' in params and 'end_date' in params:
            try:
                start = datetime.strptime(params['start_date'], '%Y-%m-%d').date()
                end = datetime.strptime(params['end_date'], '%Y-%m-%d').date()
                main_filter &= Q(enrollment_date__range=[start, end])
            except ValueError:
                pass

        # Фильтрация по кафедрам и программам
        if 'current_departments' in params:
            departments = params['current_departments'].split(',')
            main_filter &= Q(current_department_id__in=departments)

        if 'current_programs' in params:
            programs = params['current_programs'].split(',')
            main_filter &= Q(current_program_id__in=programs)

        # Фильтрация по типу обучения и основанию
        if 'education_types' in params:
            types = params['education_types'].split(',')
            main_filter &= Q(education_type__in=types)

        if 'admission_bases' in params:
            bases = params['admission_bases'].split(',')
            main_filter &= Q(admission_basis__in=bases)

        # Фильтрация по нахождению в академе
        if 'in_academic' in params:
            if params['in_academic'].lower() == 'true':
                main_filter &= Q(status='academic')

        return queryset.filter(main_filter).order_by('last_name', 'first_name')


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgramListView(generics.ListAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id', None)
        if department_id:
            try:
                department_ids = [int(id) for id in department_id.split(',')]
                return Program.objects.filter(department_id__in=department_ids)
            except (ValueError, TypeError):
                return Program.objects.none()
        return Program.objects.all()
