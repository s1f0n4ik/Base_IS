from rest_framework import serializers
from .models import Student, Department, Program


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class ProgramSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'name', 'department']


class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    education_type_display = serializers.CharField(source='get_education_type_display', read_only=True)
    admission_basis_display = serializers.CharField(source='get_admission_basis_display', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        extra_fields = ['education_type_display', 'admission_basis_display']