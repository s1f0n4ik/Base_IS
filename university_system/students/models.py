# models.py
from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.faculty})"


class Student(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    enrollment_date = models.DateField()
    expulsion_date = models.DateField(null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    citizenship = models.CharField(max_length=50)
    course = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"