import os
import django
import random
from faker import Faker
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_system.settings')
django.setup()

from students.models import Department, Program, Student

fake = Faker('ru_RU')


def create_departments_and_programs():
    departments = [
        {'name': 'Кафедра информатики'},
        {'name': 'Кафедра математики'},
        {'name': 'Кафедра физики'},
        {'name': 'Кафедра экономики'},
        {'name': 'Кафедра лингвистики'},
    ]

    programs_data = {
        'Кафедра информатики': ['Программная инженерия', 'Искусственный интеллект'],
        'Кафедра математики': ['Прикладная математика', 'Теоретическая математика'],
        'Кафедра физики': ['Ядерная физика', 'Квантовая механика'],
        'Кафедра экономики': ['Финансы', 'Менеджмент'],
        'Кафедра лингвистики': ['Английская филология', 'Переводоведение'],
    }

    for dept_data in departments:
        dept, created = Department.objects.get_or_create(name=dept_data['name'])

        for program_name in programs_data[dept.name]:
            Program.objects.get_or_create(
                name=program_name,
                department=dept
            )

    print("Созданы кафедры и направления")


def create_students(num_students=200):
    departments = Department.objects.all()
    programs = Program.objects.all()
    citizenships = ['Россия', 'Казахстан', 'Беларусь', 'Узбекистан', 'Армения']
    education_types = ['budget', 'contract']
    admission_bases = ['general', 'target', 'quota']

    for _ in range(num_students):
        dept = random.choice(departments)
        program = random.choice(programs.filter(department=dept))

        enrollment_date = fake.date_between_dates(
            date_start=datetime(2018, 1, 1),
            date_end=datetime(2023, 12, 31)
        )

        # 30% студентов отчислены
        if random.random() < 0.3:
            expulsion_date = fake.date_between_dates(
                date_start=enrollment_date,
                date_end=datetime(2023, 12, 31)
            )
        else:
            expulsion_date = None

        Student.objects.create(
            last_name=fake.last_name(),
            first_name=fake.first_name(),
            middle_name=fake.middle_name(),
            enrollment_date=enrollment_date,
            expulsion_date=expulsion_date,
            department=dept,
            program=program,
            citizenship=random.choice(citizenships),
            course=random.randint(1, 6),
            education_type=random.choice(education_types),
            admission_basis=random.choice(admission_bases)
        )

    print(f"Создано {num_students} студентов")


if __name__ == '__main__':
    create_departments_and_programs()
    create_students(300)