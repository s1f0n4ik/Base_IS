# serializers.py
from rest_framework import serializers
from .models import Student, Faculty, Program


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']


class ProgramSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'name', 'faculty']


class StudentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    program = ProgramSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'