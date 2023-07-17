from django.urls import path
from .views import *

urlpatterns = [

    # teacher endpoints
    path('teacher/',teacher_list_view,name='teacher-list'), 
    
    # student endpoints
    path('student/',student_list_view,name='student-list'),
    
    # category endpoints
    path('category/',category_list_view,name='category-list'),
    path('category/create/',category_create_view,name='category-create'),
    path('category/<int:pk>/',category_detail_view,name='category-detail'),
    path('category/<int:pk>/update/',category_update_view,name='category-update'),
    path('category/<int:pk>/delete/',category_destroy_view,name='category-delete'),
    
    # course endpoints
    path('course/',course_list_view,name='course-list'),
    path('course/create/',course_create_view,name='course-create'),
    path('course/<int:pk>/',course_detail_view,name='course-detail'),
    path('course/<int:pk>/update/',course_update_view,name='course-update'),
    path('course/<int:pk>/delete/',course_destroy_view,name='course-delete'),
    
    # course content endpoints
    path('course_content/',course_content_apiview,name='course-content-list'),# all course content endpoint
    path('course/<int:course_pk>/content/', course_content_filter_view, name='course-content-filter'), # content based on the course id
    path('course/<int:course_pk>/content/<int:pk>/', course_content_detail_view, name='course-content-detail'),
    path('course/<int:course_pk>/content/create/', course_content_create_view, name='course-content-create'),
    path('course/<int:course_pk>/content/<int:pk>/update/', course_content_update_view, name='course-content-update'),
    path('course/<int:course_pk>/content/<int:pk>/delete/', course_content_destroy_view, name='course-content-delete'),
    
    # student course purchase
    path('purchase/<int:course_id>/',course_purchase_view , name='course-purchase'),
    path('student/<int:student_id>/courses/', student_course_view, name='student-courses'),
    
    # search 
    path('', CourseSearchView.as_view(), name='search')
    
]
