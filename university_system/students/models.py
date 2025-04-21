from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.department})"


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

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    enrollment_date = models.DateField()
    expulsion_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    citizenship = models.CharField(max_length=50)
    course = models.PositiveSmallIntegerField()
    education_type = models.CharField(max_length=10, choices=EDUCATION_TYPE_CHOICES)
    admission_basis = models.CharField(max_length=10, choices=ADMISSION_BASIS_CHOICES)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"