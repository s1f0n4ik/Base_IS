# serializers.py
from rest_framework import serializers
from .models import Student, Faculty, Program


class StudentSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField()
    program = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = '__all__'