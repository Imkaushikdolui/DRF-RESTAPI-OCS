from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apiauth.models import Account
from .models import *
from django.conf import settings
from rest_framework.exceptions import ValidationError


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'pk',
            'name',
            'teacher_id'
        ]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'pk',
            'name',
            'student_id'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'pk',
            'name'
        ]


class CourseSerializer(serializers.ModelSerializer):
    course_post_date = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d--%T%H:%M:%S%z")

    class Meta:
        model = Course
        fields = [
            'pk',
            'name',
            'price',
            'course_post_date',
            'teacher',
            'category',
            'body',
            'duration',
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    course_post_date = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d--%T%H:%M:%S%z")
    teacher = TeacherSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            'pk',
            'name',
            'price',
            'course_post_date',
            'teacher',
            'category',
            'body',
            'duration',
        ]

class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_content
        fields = [
            'pk',
            'content',
            'name',
            'body',
            'course_id',
        ]

class CourseContentDetailSerializer(serializers.ModelSerializer):
    course_id = CourseDetailSerializer(read_only=True)

    class Meta:
        model = Course_content
        fields = [
            'content',
            'name',
            'body',
            'course_id',
        ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        