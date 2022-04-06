from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth  import get_user_model
from django.core.validators import FileExtensionValidator
from school.models import * #Profile, Novel, Course , Course_Description ,Cimage , Genre, Select_course,Course_category,
User = get_user_model()

from django.http import JsonResponse


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required field.')
    email = forms.EmailField(required=True,max_length=254, help_text='Required. Inform a valid email address.'
    , widget = forms.EmailInput(attrs = {'class':"styled-input"}))
    password1 = forms.CharField(max_length=30, required=True, help_text='Required field.',widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30, required=True, help_text='Required field.',widget=forms.PasswordInput())
    

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email_data = self.cleaned_data.get('email')
        email_data=email_data.lower()
        if User.objects.filter(email=email_data).exists():
            raise forms.ValidationError("This email already used")
        return email_data
    def clean_password(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 != pass2:
            raise forms.ValidationError('Enter same Password')
        return pass1


class Login(forms.Form):
    username = forms.CharField(max_length=30, required=True, help_text='Required field.')
    password1 = forms.CharField(max_length=30, required=True, help_text='Required field.', widget=forms.PasswordInput())



    






class EditProfileImageForm(ModelForm):
    profile_image = forms.ImageField(validators= [valid_image,valid_image_mimetype,valid_size])
    class Meta:
        model = Profile
        fields = ('profile_image',)
    def has_changed(self, *args, **kwargs):
        return True 
   
class EditProfileForm(ModelForm):
    profile_image = forms.FileField(validators=[valid_image,valid_image_mimetype,valid_size])
    about_me = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':"form-control",'rows':5,'cols':20}))
    instagram = forms.CharField(max_length = 30,  help_text='Your instagram username' , 
   widget=forms.TextInput( attrs = {'class':"styled-input",  'placeholder':"instagram"} ) )
    twitter = forms.CharField(max_length = 30,  help_text='Your twitter username' , 
   widget=forms.TextInput( attrs = {'class':"styled-input",  'placeholder':"twitter"} ) )

    class Meta:
        model = Profile

        fields = ['about_me' ,'profile_image', 'instagram', 'twitter' ]
    def has_changed(self, *args, **kwargs):
        return True

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['favorite'].queryset = Novel.objects.filter(created_author=user)


class Search(forms.Form):
    bar = forms.CharField(max_length=10, required=True, help_text='Required field.',
    widget = forms.TextInput(attrs={
        'class':"form-control mr-sm-2",
        'placeholder':"Search here.."
    }))





class ProfileForm(ModelForm):
    profile_image = forms.ImageField(
        label= 'Your Profile Picture',
        widget= forms.FileInput,
        validators= [valid_image,valid_image_mimetype,valid_size])
    authorName =  forms.CharField(max_length = 30, required=True, help_text='Required field' , 
   widget=forms.TextInput( attrs = {'class':"form-control",  'placeholder':"Your Name"} ) )
    about_me = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':"form-control",'placeholder':'write something catchy','rows':5,'cols':20}))
    
    class Meta:
        model = Profile
        fields = [ 'about_me' , 'authorName', 'profile_image']
    

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(ProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['favorite'].queryset = Novel.objects.filter(created_author=user)


# class Tutorial(ModelForm):
    

#     class Meta:
#         model = Course_Description
#         fields = ['course_name','course_category', 'premium' , 'description',  ]

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super(Tutorial, self).__init__(*args, **kwargs)
#         self.fields['course_name'].queryset = Select_course.objects.filter(users=user)
#         self.fields['course_name'].widget_attrs= {'class':"category2"}
   


class TutCourse(ModelForm):

    class Meta:
        model = Topics
        fields = ['title']






class PaymentForm(forms.Form):
    Email = forms.EmailField(required=False,widget = forms.EmailInput(attrs = {'class':"form-control", 'id':'email'}))
    Name = forms.CharField(max_length=30, required=True, help_text='Required field.',
    widget=forms.TextInput( attrs = {'class':"form-control",  'placeholder':"Your Name", 'id':'firstname'} ))
    LastName = forms.CharField(max_length=30, required=True, help_text='Required field.', widget=forms.TextInput( attrs = {'class':"form-control",  'id':"last-name"} ))
    def clean_email(self):
        email_data = self.cleaned_data.get('email')
        email_data=email_data.lower()
        if User.objects.filter(email=email_data).exists():
            raise forms.ValidationError("This email already used")
        return email_data




class Cancel(forms.Form):
    email = forms.EmailField(required=True,max_length=254, help_text='Required. Inform a valid email address.'
    , widget = forms.EmailInput(attrs = {'class':"styled-input"}))




# class QuestionForm(forms.Form):
#     course = forms.ChoiceField(
#         choices = [(x.id,x.course_name) for x in Course_Description.objects.all()],
#         label = 'Select Course',
#         widget = forms.Select(attrs= {'class':"category2"}),
#         required=True,
#         error_messages =  {'required': 'Select course'}
#        #
#     )
#     quiz_description = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':'form-control rounded-0','rows':10}))

#     question = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':'form-control rounded-0','rows':10}))

#     option1 =  forms.CharField(max_length=10, required=True ,
#     widget =forms.TextInput( attrs ={'class' :"styled-input"}))
#     option2 =  forms.CharField(max_length=10, required=True ,
#     widget =forms.TextInput( attrs ={'class' :"styled-input"}))
#     option3 =  forms.CharField(max_length=10, required=True ,
#     widget =forms.TextInput( attrs ={'class' :"styled-input",}))
#     option4 =  forms.CharField(max_length=10, required=True ,
#     widget =forms.TextInput( attrs ={'class' :"styled-input", }))
#     answer = forms.ChoiceField(
#         choices = [(1,'option 1'), (2,'option 2'), 
#         (3,'option 3'), (4,'option 4')],
#         required = True,
#         widget =forms.Select( attrs ={'class':"category2" })
#        #
#     )

#     feedback = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':'form-control rounded-0','rows':10}))