from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from swift.forms.course import CourseForm
from swift.helper import renderfile, is_ajax, LogUserActivity
from swift.models import Course,Curriculum
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import render, get_object_or_404, redirect
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ
from django.db import transaction



# class CourseView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
       
        
#         filterss = Curriculum.objects.all()
#         if 'curriculum' in request.GET:
#             filters = request.GET.get('curriculum')
#             print(filters)
#             courses = Course.objects.filter(name__icontains=filters).order_by('-id')
#             print(courses)

           

#         if 'filter' in request.GET:
#             filter = request.GET.get('filter')
#             courses = Course.objects.filter(name__icontains=filter).order_by('-id')
      
#             return JsonResponse(response)
      
            
#         else:
#             courses = Course.objects.filter(is_active=True).order_by('-id')
#         context, response = {}, {}
#         page = int(request.GET.get('page', 1))
#         paginator = Paginator(courses, PAGINATION_PERPAGE)
#         try:
#             courses = paginator.page(page)
#         except PageNotAnInteger:
#             courses = paginator.page(1)
#         except EmptyPage:
#             courses = paginator.page(paginator.num_pages)

#         context['courses'], context['current_page'],context['curriculums']  = courses, page ,filterss
         
#         if is_ajax(request=request):
#             response['status'] = True
#             response['pagination'] = render_to_string("swift/course/pagination.html",context=context,request=request)
#             response['template'] = render_to_string('swift/course/course_list.html', context, request=request)
#             return JsonResponse(response)
#         context['form']  = CourseForm()
#         return renderfile(request, 'course', 'index', context)
    
class CourseView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        filterss = Curriculum.objects.all()
        courses = Course.objects.filter(is_active=True).order_by('-id')
        context = {
            'courses': None,
            'current_page': None,
            'curriculums': filterss,
            'form': CourseForm()
        }
        response = {}
        if 'filter' in request.GET:
            filter_value = request.GET.get('filter')
            if filter_value:
                     courses = courses.filter(name__icontains=filter_value).order_by('-id')

        if 'curriculum' in request.GET:
            filters = request.GET.get('curriculum')
            if filters:
                     courses = courses.filter(curriculum_id=filters).order_by('-id')


        

        page = request.GET.get('page')
        paginator = Paginator(courses, PAGINATION_PERPAGE)

        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        context['courses'] = courses
        context['current_page'] = page

        if  is_ajax(request=request):
            response['status'] = True
            response['pagination'] = render_to_string("swift/course/pagination.html", context=context, request=request)
            response['template'] = render_to_string('swift/course/course_list.html', context=context, request=request)
            return JsonResponse(response)

        return render(request, 'swift/course/index.html', context)


class CourseCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = CourseForm()
        print("hi")
    
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['title'] = 'Add Course'
        data['template'] = render_to_string('swift/course/course_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = CourseForm(request.POST or None)
        if form.is_valid():
            try:
                # with transaction.atomic():
                    name = request.POST.get('name', None)
                    curriculum = request.POST.get('curriculum',None)
                    # CHECK THE DATA EXISTS
                    if not Course.objects.filter(name=name).exists():
                        obj = Course.objects.create(name=name,curriculum_id=curriculum)

                        # log entry
                        log_data = {}
                        log_data['module_name'] = 'course'
                        log_data['action_type'] = CREATE
                        log_data['log_message'] = 'Course Created'
                        log_data['status'] = SUCCESS
                        log_data['model_object'] = obj
                        log_data['db_data'] = {'name':name}
                        # log_data['db_data'] = {'course':course}
                        

                        log_data['app_visibility'] = True
                        log_data['web_visibility'] = True
                        log_data['error_msg'] = ''
                        log_data['fwd_link'] = '/course/'
                        LogUserActivity(request, log_data)

                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Course Already exists'

            except Exception as error:
                log_data = {}
                log_data['module_name'] = 'Course'
                log_data['action_type'] = CREATE
                log_data['log_message'] = 'Course updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = error
                log_data['fwd_link'] = '/course/'
                LogUserActivity(request, log_data)

                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Course'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/course/course_form.html', context, request=request)
        return JsonResponse(response)

    
class CourseUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        data = {}
        obj = get_object_or_404(Course, id = id)
        form = CourseForm(instance=obj)
        context = {'form': form, 'id': id}
        data['status'] = True
        data['title'] = 'Edit course'
        data['template'] = render_to_string('swift/course/course_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data, response = {} , {}
        id = kwargs.get('pk', None)
        obj = get_object_or_404(Course, id=id)
        previous_name = obj.name
        form = CourseForm(request.POST or None, instance=obj)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if Course.objects.filter(name__icontains=request.POST.get('name')).exclude(id=id).exists():
                        response['status'] = False
                        response['message'] = "Name already exists"
                        return JsonResponse(response)
                    obj.name = request.POST.get('name' or None)
                    obj.description = request.POST.get('description' or None)
                    obj.save()

                    # log entry
                    log_data = {}
                    log_data['module_name'] = 'Course'
                    log_data['action_type'] = UPDATE
                    log_data['log_message'] = 'Course Updated'
                    log_data['status'] = SUCCESS
                    log_data['model_object'] = obj
                    log_data['db_data'] = {'previous_name':previous_name,'updated_name':obj.name}
                    log_data['app_visibility'] = True
                    log_data['web_visibility'] = True
                    log_data['error_msg'] = ''
                    log_data['fwd_link'] = '/course/'
                    LogUserActivity(request, log_data)

                    response['status'] = True
                    response['message'] = "Course updated successfully"
                    return JsonResponse(response)
                
            except Exception as dberror:
                log_data = {}
                log_data['module_name'] = 'Course'
                log_data['action_type'] = UPDATE
                log_data['log_message'] = 'Course updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = dberror
                log_data['fwd_link'] = '/course/'
                LogUserActivity(request, log_data)

                response['message'] = "Something went wrong"
                response['status'] = True
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Course'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/course/course.html', context, request=request)
            return JsonResponse(response)
        
        
class CourseDelete(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        response = {}
        obj = get_object_or_404(Course, id = id)
        obj.is_active = False
        obj.save()

        # log entry
        log_data = {}
        log_data['module_name'] = 'Course'
        log_data['action_type'] = DELETE
        log_data['log_message'] = f'Deleted Course {obj.name}'
        log_data['status'] = SUCCESS
        log_data['model_object'] = None
        log_data['db_data'] = {'name':obj.name}
        log_data['app_visibility'] = True
        log_data['web_visibility'] = True
        log_data['error_msg'] = ''
        log_data['fwd_link'] = '/Course/'
        LogUserActivity(request, log_data)

        response['status'] = True
        response['message'] = "Course deleted successfully"
        return JsonResponse(response)