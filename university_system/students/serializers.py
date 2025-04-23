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
        fields = ['id', 'name', 'code', 'department']


class StudentSerializer(serializers.ModelSerializer):
    current_department = DepartmentSerializer(read_only=True)
    current_program = ProgramSerializer(read_only=True)
    initial_department = DepartmentSerializer(read_only=True)
    initial_program = ProgramSerializer(read_only=True)

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    education_type_display = serializers.CharField(source='get_education_type_display', read_only=True)
    admission_basis_display = serializers.CharField(source='get_admission_basis_display', read_only=True)
    expulsion_reason_display = serializers.CharField(source='get_expulsion_reason_display', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
