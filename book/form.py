from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from school.models import Profile, Novel, Course , Feedback, Course_Description ,Cimage , Genre, Select_course
from phonenumber_field.formfields import PhoneNumberField




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
     summary = forms.CharField(required = True,widget=forms.Textarea(attrs={'class':"form-control",'rows':5,'cols':20}))
     genre = forms.MultipleChoiceField(
        choices = [(x.id,x.name) for x in Genre.objects.all()],
        widget = forms.CheckboxSelectMultiple(),
        label = 'Select Genres',
        required=True,
        error_messages =  {'required': 'Genre can Be Multiple '}
       #
    )
     bookFile = forms.FileField(
         required=True,
         error_messages =  {'required': 'upload pdf,.docx,doc format'}
     )
    
   
    
 
     class Meta:
         model = Novel
         fields = ['title','isbn','bookImage','summary', 'genre','bookFile']

    






class EditProfileImageForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('profile_image',)
    def has_changed(self, *args, **kwargs):
        return True 
   
class EditProfileForm(ModelForm):
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
        choices = [(x.id,x.sel) for x in Select_course.objects.all()],
        widget = forms.CheckboxSelectMultiple(),
        label = 'Select Courses',
        required=True,
        error_messages =  {'required': 'Select with control on laptops '}
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
    Phone  =  PhoneNumberField(widget=forms.TextInput(attrs={'class':"form-control",'type':'tel','placeholder': 'Phone'}), label="Phone number", required=False)
    
     
    category1 = forms.ChoiceField(
        choices = [('first','Hours: 8am - 10am'), ('secound','Hours: 10am - 12pm'), 
        ('third','Hours: 12pm - 4pm'), ('fourth','Hours: 4pm - 7pm'),('fifth','Hours: 7pm - 9pm')],
        required = True,
        widget =forms.Select( attrs ={'class':"category2" })
       #
    )

    city =  forms.CharField(max_length=10, required=True ,help_text='start from 2nd',
    widget =forms.TextInput( attrs ={'class' :"header"}))

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
        fields = ['course_name', 'premium' , 'description', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(Tutorial, self).__init__(*args, **kwargs)
        self.fields['course_name'].queryset = Select_course.objects.filter(users=user)

class TutCourse(ModelForm):
    sel = forms.CharField(max_length = 30, required=True, help_text='Required field' )
    class Meta:
        model = Select_course
        fields = ['sel']

class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'