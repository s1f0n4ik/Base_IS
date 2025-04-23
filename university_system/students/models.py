from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название кафедры")
    code = models.CharField(max_length=20, blank=True, verbose_name="Код кафедры")

    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


class ProgramGroup(models.Model):
    code = models.CharField(max_length=20, verbose_name="Код группы")
    name = models.CharField(max_length=200, verbose_name="Название группы специальностей")

    def __str__(self):
        return f"{self.code} - {self.name}"


class Program(models.Model):
    EDUCATION_LEVELS = [
        ('undergraduate', 'Бакалавриат'),
        ('graduate', 'Магистратура'),
        ('postgraduate', 'Аспирантура'),
    ]

    code = models.CharField(max_length=20, verbose_name="Код специальности")
    old_code = models.CharField(max_length=20, blank=True, verbose_name="Старый шифр")
    name = models.CharField(max_length=200, verbose_name="Направление подготовки")
    program_name = models.CharField(max_length=300, verbose_name="Образовательная программа")
    group = models.ForeignKey(ProgramGroup, on_delete=models.SET_NULL, null=True, verbose_name="Группа специальностей")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Кафедра")
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS, verbose_name="Уровень образования")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return f"{self.code} - {self.name}: {self.program_name}"


class Student(models.Model):
    EDUCATION_TYPE_CHOICES = [
        ('budget', 'Бюджет'),
        ('contract', 'Контракт'),
    ]

    ADMISSION_BASIS_CHOICES = [
        ('general', 'Общий конкурс'),
        ('target', 'Целевое'),
        ('quota', 'Квота'),
    ]

    STATUS_CHOICES = [
        ('active', 'Обучается'),
        ('academic', 'В академе'),
        ('graduated', 'Выпускник'),
        ('expelled', 'Отчислен'),
    ]

    EXPULSION_REASON_CHOICES = [
        ('own_desire', 'По собственному желанию'),
        ('transfer', 'По переводу'),
        ('academic_failure', 'За недобросовестное освоение программы'),
        ('other', 'Другая причина'),
    ]

    # Основная информация
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    citizenship = models.CharField(max_length=50, verbose_name="Гражданство")

    # Текущий статус
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    current_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,
                                         related_name='current_students', verbose_name="Текущая кафедра")
    current_program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True,
                                      related_name='current_students', verbose_name="Текущая программа")

    # Информация о зачислении
    enrollment_date = models.DateField(verbose_name="Дата зачисления")
    initial_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,
                                         related_name='initial_students', verbose_name="Первоначальная кафедра")
    initial_program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True,
                                      related_name='initial_students', verbose_name="Первоначальная программа")
    education_type = models.CharField(max_length=10, choices=EDUCATION_TYPE_CHOICES, verbose_name="Тип обучения")
    admission_basis = models.CharField(max_length=10, choices=ADMISSION_BASIS_CHOICES, verbose_name="Основание поступления")

    # Информация об отчислении/выпуске
    expulsion_date = models.DateField(null=True, blank=True, verbose_name="Дата отчисления")
    expulsion_reason = models.CharField(max_length=20, choices=EXPULSION_REASON_CHOICES,
                                      blank=True, null=True, verbose_name="Причина отчисления")
    graduation_date = models.DateField(null=True, blank=True, verbose_name="Дата выпуска")

    # Информация об академе
    academic_leave_start = models.DateField(null=True, blank=True, verbose_name="Начало академа")
    academic_leave_end = models.DateField(null=True, blank=True, verbose_name="Конец академа")

    # История переводов
    transfer_history = models.JSONField(default=list, blank=True,
                                      verbose_name="История переводов")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name', 'middle_name']