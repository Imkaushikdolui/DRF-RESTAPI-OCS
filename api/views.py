from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q



# TEACHER APIViews


class TeacherListAPIView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


teacher_list_view = TeacherListAPIView.as_view()

# STUDENT APIViews


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


student_list_view = StudentListAPIView.as_view()

# CATEGORY APIViews


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


category_list_view = CategoryListAPIView.as_view()


class CategoryCreateAPIView(generics.CreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


category_create_view = CategoryCreateAPIView.as_view()


class CategoryDetailAPIView(generics.RetrieveAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


category_detail_view = CategoryDetailAPIView.as_view()


class CategoryUpdateAPIView(generics.UpdateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()


category_update_view = CategoryUpdateAPIView.as_view()


class CategoryDestroyAPIView(generics.DestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()


category_destroy_view = CategoryDestroyAPIView.as_view()

# COURSE APIViews


class CourseListAPIView(generics.ListAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


course_list_view = CourseListAPIView.as_view()


class CourseCreateAPIView(generics.CreateAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


course_create_view = CourseCreateAPIView.as_view()


class CourseDetailAPIView(generics.RetrieveAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


course_detail_view = CourseDetailAPIView.as_view()


class CourseUpdateAPIView(generics.UpdateAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()


course_update_view = CourseUpdateAPIView.as_view()


class CourseDestroyAPIView(generics.DestroyAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()


course_destroy_view = CourseDestroyAPIView.as_view()


# COURSE CONTENT APIViews

class CouseContentAPIView(generics.ListAPIView):
    queryset = Course_content.objects.all()
    serializer_class = CourseContentSerializer


course_content_apiview = CouseContentAPIView.as_view()


class CourseContentFilterAPIView(generics.ListAPIView):
    serializer_class = CourseContentSerializer

    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        queryset = Course_content.objects.filter(course_id=course_pk)
        return queryset


course_content_filter_view = CourseContentFilterAPIView.as_view()


class CourseContentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CourseContentDetailSerializer

    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        content_pk = self.kwargs['pk']
        queryset = Course_content.objects.filter(
            course_id=course_pk, pk=content_pk)
        return queryset


course_content_detail_view = CourseContentDetailAPIView.as_view()


class CourseContentCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseContentSerializer

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        course = Course.objects.get(pk=course_id)
        serializer.save(course_id=course)


course_content_create_view = CourseContentCreateAPIView.as_view()


class CourseContentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseContentSerializer

    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        queryset = Course_content.objects.filter(course_id=course_pk)
        return queryset


course_content_update_view = CourseContentUpdateAPIView.as_view()


class CourseContentDeleteAPIView(generics.DestroyAPIView):

    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        queryset = Course_content.objects.filter(course_id=course_pk)
        return queryset


course_content_destroy_view = CourseContentDeleteAPIView.as_view()

class PurchaseAPIView(APIView):
    def post(self, request, course_id, *args, **kwargs):
        try:
            student_id = request.data.get('student_id')
            if not student_id:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Student ID is required.',
                    'data': {}
                })

            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return Response({
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Student not found!',
                    'data': {}
                })

            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                return Response({
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Course not found!',
                    'data': {}
                })

            teacher = course.teacher
            price = course.price

            # Create a new Purchase object
            purchase = Payment.objects.create(
                student_id=student,
                teacher_id=teacher,
                course_id=course,  # Assign the course object instead of course_id
                payment_price=price
            )


            # Add any additional logic or validation here

            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Purchase successful!',
                'data': {
                    'student_id': student_id,
                    'teacher_id': teacher.id,
                    'course_id': course_id,
                    'payment_price': price
                }
            })

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An error occurred during purchase.',
                'data': {'error': str(e)}
            })

course_purchase_view = PurchaseAPIView.as_view()

class StudentCoursesAPI(APIView):
    def get(self, request, student_id, *args, **kwargs):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Student not found!',
                'data': {}
            })

        courses = Course.objects.filter(payment__student_id=student_id)
        serializer = CourseSerializer(courses, many=True)

        course_ids = courses.values_list('id', flat=True)
        contents = Course_content.objects.filter(course_id__in=course_ids)
        content_serializer = CourseContentDetailSerializer(contents, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Courses purchased by the student.',
            'data': {
                'student_id': student_id,
                'student_name': student.name,
                'courses': serializer.data,
                'contents': content_serializer.data
            }
        })

student_course_view = StudentCoursesAPI.as_view()



class CourseSearchView(generics.ListAPIView):
    serializer_class = CourseDetailSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        query = self.request.GET.get('q')
        if query:
            lookup = Q(name__icontains=query) | Q(body__icontains=query)
            queryset = queryset.filter(lookup)
        return queryset














































