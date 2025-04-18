# populate_db.py
import os
import django
import random
from faker import Faker
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_system.settings')
django.setup()

from students.models import Faculty, Program, Student

fake = Faker('ru_RU')


def create_faculties_and_programs():
    faculties = [
        {'name': 'Инженерный факультет'},
        {'name': 'Факультет экономики'},
        {'name': 'Гуманитарный факультет'},
        {'name': 'Факультет информационных технологий'},
        {'name': 'Медицинский факультет'},
    ]

    programs_data = {
        'Инженерный факультет': ['Механика', 'Строительство', 'Электротехника'],
        'Факультет экономики': ['Экономика', 'Менеджмент', 'Финансы'],
        'Гуманитарный факультет': ['История', 'Философия', 'Филология'],
        'Факультет информационных технологий': ['Компьютерные науки', 'Кибербезопасность', 'Искусственный интеллект'],
        'Медицинский факультет': ['Лечебное дело', 'Стоматология', 'Фармация'],
    }

    for faculty_data in faculties:
        faculty, created = Faculty.objects.get_or_create(name=faculty_data['name'])

        for program_name in programs_data[faculty.name]:
            Program.objects.get_or_create(
                name=program_name,
                faculty=faculty
            )

    print("Созданы факультеты и направления")


def create_students(num_students=100):
    faculties = Faculty.objects.all()
    programs = Program.objects.all()
    citizenships = ['Россия', 'Казахстан', 'Беларусь', 'Узбекистан', 'Армения', 'Азербайджан']

    for _ in range(num_students):
        faculty = random.choice(faculties)
        program = random.choice(programs.filter(faculty=faculty))

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
            faculty=faculty,
            program=program,
            citizenship=random.choice(citizenships),
            course=random.randint(1, 6)
        )

    print(f"Создано {num_students} студентов")


if __name__ == '__main__':
    create_faculties_and_programs()
    create_students(200)  # Создаем 200 студентов для тестов