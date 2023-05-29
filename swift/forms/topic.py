from django import forms

from swift.models import Subject,Course,Topic



class TopicForm(forms.ModelForm):
    name = forms.CharField(
        label="Title", max_length=200, required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
        error_messages={'required': 'The name should not be empty'}
    )
    course = forms.ModelChoiceField(
        label="Course", widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Course.objects.all(),
        
     
        required=True,
       
        error_messages={'required': 'The course should not be empty'}
    )
    subject = forms.ModelChoiceField(
        
        label="Subject", widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Subject.objects.none(),  # Initially set an empty queryset
        required=True,
        error_messages={'required': 'The subject should not be empty'}
    )

    class Meta:
        model = Topic
        fields = ["name", "course", "subject"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'course' in self.data:  # Check if 'course' field is present in the submitted form data
            try:
                course_id = int(self.data.get('course'))
                self.fields['subject'].queryset = Subject.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:  # Check if the form is for an existing instance (during editing)
            self.fields['subject'].queryset = self.instance.course.subjects.all()

    # def __init__(self, *args, **kwargs):
    #     super(TopicForm, self).__init__(*args, **kwargs)
    #     self.fields['course_id'].widget = forms.HiddenInput()

    #     instance = kwargs.get('instance', None)
    #     if instance:
    #         self.fields['subject_id'].queryset = Subject.objects.filter(course_id=instance.course_id)

# class TopicForm(forms.ModelForm):
#     name = forms.CharField( 
#         label="Title", max_length=200, required = True,
#         widget=forms.TextInput(attrs={'autocomplete':'off'}),
#         error_messages={ 'required': 'The name should not be empty' }
#     )
#     course = forms.ModelChoiceField(
#         label="course",widget=forms.Select(attrs={'class':'form-control'}),
#         queryset=Course.objects.all(),
#         required=True,
#         error_messages={ 'required': 'The course should not be empty' }
#     )
#     subject = forms.ModelChoiceField(
#         label="subject",widget=forms.Select(attrs={'class':'form-control'}),
#         queryset=Subject.objects.all(),
#         required=True,
#         error_messages={ 'required': 'The subject should not be empty' }
#     )

#     class Meta:
#         model = Topic
#         fields = ["name","course","subject"]