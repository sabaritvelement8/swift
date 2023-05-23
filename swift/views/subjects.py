from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  View
from swift.forms.subjects import SubjectsForm
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from swift.models import Subject
from swift.helper import renderfile,is_ajax,LogUserActivity
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.db import transaction
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ

class SubjectsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        page = int(request.GET.get('page', 1))
        subjects = Subject.objects.filter(is_active=True).order_by('-id')

        paginator = Paginator(subjects, PAGINATION_PERPAGE)
        try:
            subjects = paginator.page(page)
        except PageNotAnInteger:
            subjects = paginator.page(1)
        except EmptyPage:
            subjects = paginator.page(paginator.num_pages)

        context['subjects'], context['current_page'] = subjects, page
        if is_ajax(request=request):
            response['status'] = True
            response['pagination'] = render_to_string("swift/subject/pagination.html",context=context,request=request)
            response['template'] = render_to_string('swift/subject/subject_list.html', context, request=request)
            return JsonResponse(response)
        context['form']  = SubjectsForm()
        return renderfile(request, 'subject', 'index', context)
        # return render(request,'subject/index.html',context)




class SubjectCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = SubjectsForm()
        print("hi")
    
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['title'] = 'Add Subject'
        print("kk")
        print(data)
        data['template'] = render_to_string('swift/subject/subject_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        print("ok")
        response = {}
        form = SubjectsForm(request.POST or None)
        print("hlo")
        if form.is_valid():
            try:
                # with transaction.atomic():
                    name = request.POST.get('name', None)
                    print(name)
                    print("hello")
                    course = request.POST.get('course',None)
                    print(course)
                    # CHECK THE DATA EXISTS
                    if not Subject.objects.filter(name=name).exists():
                        obj = Subject.objects.create(name=name,course_id=course)
                        print(obj)
                        print('tt')

                        # log entry
                        log_data = {}
                        log_data['module_name'] = 'subject'
                        log_data['action_type'] = CREATE
                        log_data['log_message'] = 'Subject Created'
                        log_data['status'] = SUCCESS
                        log_data['model_object'] = obj
                        log_data['db_data'] = {'name':name}
                        # log_data['db_data'] = {'course':course}
                        

                        log_data['app_visibility'] = True
                        log_data['web_visibility'] = True
                        log_data['error_msg'] = ''
                        log_data['fwd_link'] = '/subject/'
                        LogUserActivity(request, log_data)

                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Subject Already exists'

            except Exception as error:
                print("hlo ",error)
                log_data = {}
                log_data['module_name'] = 'Subject'
                log_data['action_type'] = CREATE
                log_data['log_message'] = 'Subject updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = error
                log_data['fwd_link'] = '/subject/'
                LogUserActivity(request, log_data)

                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Subject'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/subject/subject_form.html', context, request=request)
        return JsonResponse(response)