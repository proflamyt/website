from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from school.models import * #Profile, Novel, Course , Course_Description ,Cimage , Genre, Select_course,Course_category,

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


class Login(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required field.')
    password1 = forms.CharField(max_length=30, required=True, help_text='Required field.', widget=forms.PasswordInput())


class UploadBookForm(forms.ModelForm):
     title = forms.CharField(required=True,
     widget = forms.TextInput( attrs= {'class':"styled-input", 'placeholder':'Book Title'} ))

     isbn = forms.IntegerField(required=True,
     widget = forms.TextInput( attrs= {'class':"styled-input", 'placeholder':'Book Isbn'} ))
    
     bookFile = forms.FileField(validators= [valid_file,valid_pdf_mimetype,valid_size])

     bookImage = forms.ImageField(validators= [valid_image,valid_image_mimetype,valid_size])
        
     genre = forms.MultipleChoiceField(
        choices = [(x.id,x.name) for x in Genre.objects.all()],
        label = 'Select Genres',
        required=True,
        error_messages =  {'required': 'Select multiple genres '}
       #
    )
    
     summary = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':'form-control rounded-0','rows':10}))
   
    
 
     class Meta:
         model = Novel
         fields = ['title','isbn','bookImage','bookFile','genre', 'summary']

     def correct(self):
         bookFile = self.cleaned_data.get('bookFile')
         bookImage = self.cleaned_data.get('bookImage')



    






class EditProfileImageForm(ModelForm):
    profile_image = forms.ImageField(validators= [valid_image,valid_image_mimetype,valid_size])
    class Meta:
        model = Profile
        fields = ('profile_image',)
    def has_changed(self, *args, **kwargs):
        return True 
   
class EditProfileForm(ModelForm):
    profile_image = forms.FileField( validators=[valid_image,valid_image_mimetype,valid_size])
    about_me = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':"form-control",'rows':5,'cols':20}))

    class Meta:
        model = Profile

        fields = ['favorite' , 'about_me' ,'profile_image' ]
    def has_changed(self, *args, **kwargs):
        return True

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['favorite'].queryset = Novel.objects.filter(created_author=user)


class Search(forms.Form):
    bar = forms.CharField(max_length=10, required=True, help_text='Required field.',
    widget = forms.TextInput(attrs={
        'class':"form-control mr-sm-2",
        'placeholder':"Search here.."
    }))



class Courses(ModelForm):
    coursess = forms.MultipleChoiceField(
        choices = [(x.id,x.category) for x in Course_category.objects.all()],
        widget = forms.CheckboxSelectMultiple(),
        label = 'Select Courses',
        required=True,
        error_messages =  {'required': 'Select multiple courses '}
       #
    )
    name = forms.CharField(max_length = 30, required=True, help_text='Required field' , 
   widget=forms.TextInput( attrs = {'class':"styled-input",  'placeholder':"Your Name"} ) )
    gender = forms.ChoiceField(
        choices = [("",'Gender'), ('0','Female'),( '1','Male'), ('2','Other')],
        required = True,
        widget = forms.Select( attrs= {'class':"category2"})
       #
    )
    Phone  =  forms.CharField(max_length=14, required=True ,help_text='start from 2nd',
    widget = forms.TextInput( attrs= {'class':"styled-input", 'placeholder':'+2348.......'}))
    
     
    category1 = forms.ChoiceField(
        choices = [('first','Hours: 8am - 10am'), ('secound','Hours: 10am - 12pm'), 
        ('third','Hours: 12pm - 4pm'), ('fourth','Hours: 4pm - 7pm'),('fifth','Hours: 7pm - 9pm')],
        required = True,
        widget =forms.Select( attrs ={'class':"category2" })
       #
    )

    city =  forms.CharField(max_length=10, required=True ,help_text='start from 2nd',
    widget =forms.TextInput( attrs ={'class' :"styled-input", 'placeholder':'Nationalty'}))

    date = forms.DateTimeField(
   
    widget = forms.DateTimeInput(attrs= {
        'class':'styled-input',"placeholder":"Birth Date" ,'id':"datepicker", 'onblur':"if (this.value == '') {this.value = 'mm/dd/yyyy';}", 'onfocus':"this.value = '';"})
)

    class Meta:
        model = Course
        fields = ['name','gender','Phone','category1','city','coursess', 'date', 'Email']

class ProfileForm(ModelForm):

    authorName =  forms.CharField(max_length = 30, required=True, help_text='Required field' , 
   widget=forms.TextInput( attrs = {'class':"form-control",  'placeholder':"Your Name"} ) )
    about_me = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':"form-control",'placeholder':'write something catchy','rows':5,'cols':20}))
    
    class Meta:
        model = Profile
        fields = ['favorite', 'about_me' , 'authorName', 'profile_image']
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['favorite'].queryset = Novel.objects.filter(created_author=user)


class Tutorial(ModelForm):


    class Meta:
        model = Course_Description
        fields = ['course_name','course_category', 'premium' , 'description',  ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(Tutorial, self).__init__(*args, **kwargs)
        self.fields['course_name'].queryset = Select_course.objects.filter(users=user)

class TutCourse(ModelForm):

    class Meta:
        model = Select_course
        fields = ['sel']


class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'