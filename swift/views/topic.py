from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  View
from swift.forms.topic import TopicForm
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from swift.models import Subject,Course,Topic
from swift.helper import renderfile,is_ajax,LogUserActivity
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.db import transaction
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ
from django.shortcuts import get_object_or_404


class TopicView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
       
      
        context = {
            'topic': None,
            'current_page': None,
            'subject':Subject.objects.all(),
           
        }
        response = {}
        cond = {'is_active':True}
            
        if 'filter' in request.GET:
            filter_value = request.GET.get('filter')
            if filter_value:
                cond['name__icontains']=filter_value
            
        if 'subject' in request.GET:
            filters = request.GET.get('subject')
            if filters:
                    cond['subject_id']=filters
                        

        topic = Topic.objects.select_related('subject').filter(**cond).order_by('-id')
            # return JsonResponse(response)
            
        
        
        page = int(request.GET.get('page', 1))


        paginator = Paginator(topic, PAGINATION_PERPAGE)

        try:
            topic = paginator.page(page)
        except PageNotAnInteger:
            topic = paginator.page(1)
        except EmptyPage:
            topic = paginator.page(paginator.num_pages)

        context['topic'], context['current_page'] = topic,page
        if is_ajax(request=request):
            response['status'] = True
            response['pagination'] = render_to_string("swift/topic/pagination.html",context=context,request=request)
            response['template'] = render_to_string('swift/topic/topic_list.html', context, request=request)
            return JsonResponse(response)
        
        return render(request,'swift/topic/index.html',context)



# create
class TopicCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = TopicForm()
       
    
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['title'] = 'Add Topic'
      
        data['template'] = render_to_string('swift/topic/topic_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
    
        response = {}
        form = TopicForm(request.POST or None)
       
        if form.is_valid():
            try:
                # with transaction.atomic():
                    name = request.POST.get('name', None)
               
                   
                    course = request.POST.get('course',None)
                    subject = request.POST.get('subject',None)
                    print(course)
                    # CHECK THE DATA EXISTS
                    if not Subject.objects.filter(name=name).exists():
                        obj = Subject.objects.create(name=name,subject_id=subject,course_course_id=course)
                     
                       

                        # log entry
                        log_data = {}
                        log_data['module_name'] = 'topic'
                        log_data['action_type'] = CREATE
                        log_data['log_message'] = 'Subject Created'
                        log_data['status'] = SUCCESS
                        log_data['model_object'] = obj
                        log_data['db_data'] = {'name':name}
                        # log_data['db_data'] = {'course':course}
                        

                        log_data['app_visibility'] = True
                        log_data['web_visibility'] = True
                        log_data['error_msg'] = ''
                        log_data['fwd_link'] = '/topic/'
                        LogUserActivity(request, log_data)

                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'topic Already exists'

            except Exception as error:
                print("hlo ",error)
                log_data = {}
                log_data['module_name'] = 'topic'
                log_data['action_type'] = CREATE
                log_data['log_message'] = 'topic updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = error
                log_data['fwd_link'] = '/topic/'
                LogUserActivity(request, log_data)

                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Add topic'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/topic/topic_form.html', context, request=request)
        return JsonResponse(response)