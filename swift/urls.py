from django.urls import path
from swift.views.account import *
from swift.views.curriculum import *
from swift.views.subjects import *
from swift.views.course import *

app_name = "appswift"
# views
urlpatterns = [
    # Landing Page
    path("", SignIn.as_view(), name="signin"),
    path("home/", Home.as_view(), name="home"),

    #Login Actions 
    path("signin/", SignIn.as_view(), name="signin"),
    path("forgot-password/", ForgotPassword.as_view(),name="forgot_password"),
    path("signout/", SignOut.as_view(), name="signout"),

    #Curriculum
    path("curriculum/", CurriculumView.as_view(), name="curriculum"),
    path('curriculum/create/', CurriculumCreate.as_view(), name='create_curriculum'),
    path('curriculum/<int:pk>/update/', CurriculumUpdate.as_view(), name='update_curriculum'),
    path('curriculum/<int:pk>/delete/', CurriculumDelete.as_view(), name='delete_curriculum'),

    #subject
    path("subject/", SubjectsView.as_view(), name="subject"),
    path('subject/create/', SubjectCreate.as_view(), name='create_subject'),
    path('subject/<int:pk>/update/', SubjectUpdate.as_view(), name='update_subject'),
    path('subject/<int:pk>/delete/', SubjectDelete.as_view(), name='delete_subject'),

    #Search
    path('search/', SearchResultsView.as_view(), name='search-results'),

    # Course
    path("course/", CourseView.as_view(), name="course"),
    path('course/create/', CourseCreate.as_view(), name='create_course'),
    path('course/<int:pk>/update/', CourseUpdate.as_view(), name='update_course'),
    path('course/<int:pk>/delete/', CourseDelete.as_view(), name='delete_course'),



] 