import os
import django
import pandas as pd
import random
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_system.settings')
django.setup()

from students.models import Department, ProgramGroup, Program, Student

# Инициализация Faker для генерации случайных данных
fake = Faker('ru_RU')

# Конфигурация соответствия кодов групп специальностей и кафедр
DEPARTMENT_MAPPING = {
    '1.2': 'КН',  # Компьютерные науки
    '1.3': 'РФ',  # Физические науки
    '1.4': 'ХМ',  # Химические науки
    '2.2': 'ЭЛ',  # Электроника
    '2.3': 'КН',  # Информационные технологии
    '2.4': 'ЭТ',  # Энергетика
    '2.5': 'ЭТ',  # Машиностроение (добавлено)
    '2.6': 'ХМ',  # Химические технологии (добавлено)
    '5.2': 'ЭК',  # Экономика
    '5.4': 'ЭК',  # Социология (добавлено)
    '5.5': 'ЭК',  # Политология (добавлено)
    '5.7': 'ЛГ',  # Философия (добавлено)
    '5.9': 'ЛГ',  # Филология
}


def create_departments():
    departments_data = [
        {"name": "Кафедра компьютерных наук", "code": "КН"},
        {"name": "Кафедра радиофизики", "code": "РФ"},
        {"name": "Кафедра электроники", "code": "ЭЛ"},
        {"name": "Кафедра фотоники", "code": "ФТ"},
        {"name": "Кафедра экономики", "code": "ЭК"},
        {"name": "Кафедра лингвистики", "code": "ЛГ"},
        {"name": "Кафедра химии", "code": "ХМ"},
        {"name": "Кафедра электротехники", "code": "ЭТ"},
    ]

    for dept in departments_data:
        Department.objects.get_or_create(
            code=dept["code"],
            defaults={"name": dept["name"]}
        )
    print(f"Создано {len(departments_data)} кафедр")


def create_program_groups():
    groups_data = [
        {"code": "1.2", "name": "Компьютерные науки и информатика"},
        {"code": "1.3", "name": "Физические науки"},
        {"code": "1.4", "name": "Химические науки"},
        {"code": "2.2", "name": "Электроника, фотоника, приборостроение и связь"},
        {"code": "2.3", "name": "Информационные технологии и телекоммуникации"},
        {"code": "2.4", "name": "Энергетика и электротехника"},
        {"code": "2.5", "name": "Машиностроение"},  # Добавлено
        {"code": "2.6", "name": "Химические технологии, науки о материалах, металлургия"},  # Добавлено
        {"code": "5.2", "name": "Экономика"},
        {"code": "5.4", "name": "Социологические науки"},  # Добавлено
        {"code": "5.5", "name": "Политология"},  # Добавлено
        {"code": "5.7", "name": "Философия, этика и религиоведение"},  # Добавлено
        {"code": "5.9", "name": "Филология"},
    ]

    for group in groups_data:
        ProgramGroup.objects.get_or_create(
            code=group["code"],
            defaults={"name": group["name"]}
        )
    print(f"Создано {len(groups_data)} групп специальностей")


def determine_department(code):
    """Определяет кафедру на основе кода специальности"""
    try:
        if pd.isna(code):
            return Department.objects.first()

        code_str = str(code).strip()
        if not code_str or code_str == 'nan':
            return Department.objects.first()

        # Извлекаем группу (первые две цифры)
        parts = code_str.split('.')
        if len(parts) >= 2:
            group_code = f"{parts[0]}.{parts[1]}"
        else:
            group_code = code_str

        department_code = DEPARTMENT_MAPPING.get(group_code, 'КН')
        return Department.objects.get(code=department_code)
    except Exception as e:
        print(f"Ошибка определения кафедры для кода {code}: {e}")
        return Department.objects.first()


def create_programs_from_excel(file_path):
    """Создает программы из Excel файла"""
    try:
        # Читаем Excel файл, пропуская первые 3 строки (заголовки)
        df = pd.read_excel(file_path, sheet_name='Для стипендиата', header=2)
        created_count = 0

        # Переименовываем столбцы для удобства
        df.columns = ['code', 'direction', 'old_code', 'program_name']

        for index, row in df.iterrows():
            try:
                # Пропускаем пустые строки
                if pd.isna(row['code']) and pd.isna(row['old_code']):
                    continue

                # Обрабатываем данные
                code = str(row['code']).strip() if pd.notna(row['code']) else ""
                old_code = str(row['old_code']).strip() if pd.notna(row['old_code']) else ""
                direction = str(row['direction']).strip() if pd.notna(row['direction']) else ""
                program_name = str(row['program_name']).strip() if pd.notna(row['program_name']) else ""

                # Если нет кода, но есть старый код, используем его
                if not code and old_code:
                    code = old_code.split(' ')[0] if ' ' in old_code else old_code

                # Определяем группу специальностей
                group_code = None
                if old_code and '.' in old_code:
                    group_code = '.'.join(old_code.split('.')[:2])
                elif code and '.' in code:
                    group_code = '.'.join(code.split('.')[:2])

                if not group_code:
                    print(f"Не удалось определить группу для строки {index}, пропускаем")
                    continue

                try:
                    group = ProgramGroup.objects.get(code=group_code)
                except ObjectDoesNotExist:
                    print(f"Группа {group_code} не найдена, пропускаем строку {index}")
                    continue

                # Определяем кафедру
                department = determine_department(old_code if old_code else code)

                # Создаем программу
                Program.objects.get_or_create(
                    code=code,
                    defaults={
                        'old_code': old_code,
                        'name': direction,
                        'program_name': program_name,
                        'group': group,
                        'department': department,
                        'education_level': 'postgraduate'
                    }
                )
                created_count += 1

            except Exception as e:
                print(f"Ошибка при обработке строки {index + 3}: {e}")
                continue

        print(f"Создано {created_count} программ")
        return created_count

    except Exception as e:
        print(f"Ошибка при чтении файла Excel: {e}")
        return 0


def create_random_students(num_students=50):
    """Создает тестовых студентов со случайными данными"""
    programs = list(Program.objects.all())
    departments = list(Department.objects.all())
    citizenships = ['Россия', 'Казахстан', 'Беларусь', 'Узбекистан', 'Армения']
    statuses = ['active', 'academic', 'graduated', 'expelled']
    expulsion_reasons = ['own_desire', 'transfer', 'academic_failure', 'other']

    if not programs:
        print("Нет программ для привязки студентов! Создаем временные программы...")
        # Создаем временные программы для теста
        department = Department.objects.first()
        group = ProgramGroup.objects.first()
        Program.objects.create(
            code="00.00.00",
            name="Не указано",
            program_name="Программа не указана",
            group=group,
            department=department,
            education_level='postgraduate'
        )
        programs = list(Program.objects.all())

    created_count = 0
    for _ in range(num_students):
        try:
            program = random.choice(programs)
            department = program.department

            # Основные данные
            student_data = {
                'last_name': fake.last_name(),
                'first_name': fake.first_name(),
                'middle_name': fake.middle_name(),
                'citizenship': random.choice(citizenships),
                'enrollment_date': fake.date_between_dates(
                    date_start=datetime(2018, 1, 1),
                    date_end=datetime(2023, 12, 31)
                ),
                'initial_department': department,
                'initial_program': program,
                'current_department': department,
                'current_program': program,
                'education_type': random.choice(['budget', 'contract']),
                'admission_basis': random.choice(['general', 'target', 'quota']),
                'status': random.choice(statuses),
            }

            # Для отчисленных студентов
            if student_data['status'] == 'expelled':
                student_data['expulsion_date'] = fake.date_between_dates(
                    date_start=student_data['enrollment_date'],
                    date_end=datetime(2023, 12, 31)
                )
                student_data['expulsion_reason'] = random.choice(expulsion_reasons)

            # Для выпускников
            elif student_data['status'] == 'graduated':
                student_data['graduation_date'] = fake.date_between_dates(
                    date_start=student_data['enrollment_date'],
                    date_end=datetime(2023, 12, 31)
                )

            # Для студентов в академе
            elif student_data['status'] == 'academic':
                student_data['academic_leave_start'] = fake.date_between_dates(
                    date_start=student_data['enrollment_date'],
                    date_end=datetime(2023, 12, 31)
                )
                student_data['academic_leave_end'] = fake.date_between_dates(
                    date_start=student_data['academic_leave_start'],
                    date_end=datetime(2024, 12, 31)
                )

            # История переводов (30% студентов)
            if random.random() < 0.3 and len(departments) > 1:
                new_dept = random.choice([d for d in departments if d != department])
                new_program = random.choice([p for p in programs if p.department == new_dept])
                transfer_date = fake.date_between_dates(
                    date_start=student_data['enrollment_date'],
                    date_end=datetime(2023, 12, 31)
                )

                student_data['current_department'] = new_dept
                student_data['current_program'] = new_program
                student_data['transfer_history'] = [{
                    'date': transfer_date.strftime('%Y-%m-%d'),
                    'from': program.id,
                    'to': new_program.id
                }]

            Student.objects.create(**student_data)
            created_count += 1
        except Exception as e:
            print(f"Ошибка при создании студента: {e}")

    print(f"Создано {created_count} тестовых студентов")
    return created_count


if __name__ == '__main__':
    print("Начало заполнения базы данных...")

    # Создаем кафедры
    create_departments()

    # Создаем группы специальностей
    create_program_groups()

    # Импортируем программы из Excel
    excel_file = 'Специальности (2).xlsx'
    if os.path.exists(excel_file):
        print(f"Чтение данных из файла {excel_file}...")
        create_programs_from_excel(excel_file)
    else:
        print(f"Файл {excel_file} не найден! Создаем тестовые программы...")
        # Создаем несколько тестовых программ, если файл не найден
        department = Department.objects.first()
        group = ProgramGroup.objects.first()
        Program.objects.create(
            code="01.00.00",
            name="Тестовая программа 1",
            program_name="Тестовая образовательная программа 1",
            group=group,
            department=department,
            education_level='postgraduate'
        )
        Program.objects.create(
            code="02.00.00",
            name="Тестовая программа 2",
            program_name="Тестовая образовательная программа 2",
            group=group,
            department=department,
            education_level='postgraduate'
        )

    # Создаем тестовых студентов
    print("Создание тестовых студентов...")
    create_random_students(100)  # Можно изменить количество студентов

    print("Заполнение базы данных завершено.")