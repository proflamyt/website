from statistics import mode
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
import magic
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from real import settings
import sys
from djangorave.models import TransactionModel
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.core.exceptions  import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
valid_file = FileExtensionValidator (allowed_extensions=['pdf', 'doc', 'docx' ])
valid_image = FileExtensionValidator(allowed_extensions=['jpeg','png', 'jpg'])

def get_mime(value):
    mime = magic.Magic(mime=True)
    mimetype =  mime.from_buffer(value.read(2048))
    value.seek(0)
    return mimetype

def valid_size(value):
    filesize = value.size
    if filesize > 1* 1024 * 1024:
         raise ValidationError('The maximum file size that can be uploaded is 1MB')
    else:
        return value

def valid_image_mimetype(value):
    mimetype = get_mime(value)
    if mimetype.startswith('image'):
        return value
    else:
        raise ValidationError('This Field accept only image')

def valid_pdf_mimetype(value):
    mimetype = get_mime(value)
    if 'pdf' or'msword' or'document' in mimetype : 
        return value
    else:
        return ValidationError('This Field accept only book format')



class User(AbstractUser):
    Gender = (
        ('1', 'Male'),
        ('0', 'Female'),
        
    )
    email_confirmed = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    Phone = PhoneNumberField('INTERNATIONAL')
    registered_courses = models.ManyToManyField('Course_Description')
    gender = models.CharField(max_length=2, choices=Gender)

    def __str__(self) -> str:
        return f"{self.username}"



class Profile(models.Model):
    authorName = models.CharField(max_length=200)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

    profile_image = models.ImageField(default ='default_profile.jpg', upload_to='profile/images' , validators = [valid_image,valid_image_mimetype,valid_size])   

    about_me = models.TextField(blank=True, null=True)

    instagram = models.CharField(max_length=30, null=True)

    twitter = models.CharField(max_length=30, null=True)

    

    def save(self, *args, **kwargs):
         if not self.id:
            self.profile_image = self.compress(self.profile_image)
         super(Profile, self).save(*args,**kwargs)
    def compress(self, image):
        im = Image.open(image)
        im_io = BytesIO()
        im = im.resize(( 480 ,380))
        im =im.convert('RGB')
        im.save(im_io, 'JPEG', quality=90)
        im_io.seek(0)
        profile_image = InMemoryUploadedFile(im_io,'ImageField', '%s.jpg' % image.name.split('.')[0], 'image/jpeg',sys.getsizeof(im_io), None)
        return profile_image
        
    def __str__(self):
        return f"{self.user}"

    
class Course_Description(models.Model):
    name = models.CharField(max_length=200, unique=True, null=True)
    image = models.ImageField(default ='default_profile.jpg', upload_to='courses/images' , validators = [valid_image,valid_image_mimetype,valid_size])
    description = RichTextField()
    tutor =  models.ManyToManyField('Tutor')
    ordering = models.IntegerField(unique=True,null=True,blank=True)
    class Meta:
        ordering = ['ordering',]
    def __str__(self):
        return f"{self.name}"

    



class Topics(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course_Description,related_name='course', on_delete=models.SET_NULL,blank=True, null=True)  
    texts = RichTextUploadingField()
    premium = models.BooleanField(default=False)
    
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title}"
    




class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,blank=True, null=True ,related_name='tutor')
    about = RichTextField(null=True)
    image = models.ImageField(default ='default_profile.jpg', upload_to='courses/images' , validators = [valid_image,valid_image_mimetype,valid_size])
    twitter = models.CharField(max_length=30, null=True)
    github = models.CharField(max_length=30, null=True)

    def save(self, *args, **kwargs):
         if not self.id and self.image:
            self.image = self.compress(self.image)
         super(Tutor, self).save(*args,**kwargs)
    def compress(self, image):
        im = Image.open(image)
        im_io = BytesIO()
        im = im.resize(( 480 ,380))
        im =im.convert('RGB')
        im.save(im_io, 'JPEG', quality=90)
        im_io.seek(0)
        profile_image = InMemoryUploadedFile(im_io,'ImageField', '%s.jpg' % image.name.split('.')[0], 'image/jpeg',sys.getsizeof(im_io), None)
        return profile_image
        
    def __str__(self):
        return f"{self.user}"





class Premium(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user} ----{self.premium}"

    @property
    def get_created_date(self):
        subscription = TransactionModel.objects.filter(
            user=self.user, status='successful').last()
        return subscription.created_datetime

    @property
    def get_next_billing_date(self):
       
        return self.expiry_date



class Quiz(models.Model):
    name = models.CharField(max_length=1000)
    topic = models.OneToOneField(Course_Description, null=True, on_delete=models.CASCADE)
    question_count = models.IntegerField(default=0)
    description = models.CharField(max_length=70)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    slug = models.SlugField()
    roll_out = models.BooleanField(default=False)
    class Meta:
        ordering = ['created',]
        verbose_name_plural ="Quizzes"
    def __str__(self):
        return self.name

    

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_asked = models.CharField(max_length=1000,null=True,blank=True, default='ola')
    option1 = models.CharField(max_length=100,null=True,blank=True, default='ola')
    option2 = models.CharField(max_length=100,null=True,blank=True, default='ola')
    option3 = models.CharField(max_length=100,null=True,blank=True, default='ola')
    option4 = models.CharField(max_length=100,null=True,blank=True, default='ola')
    
    def __str__(self):
        return self.question_asked

class Answer(models.Model):
    options = (
        (1, 'option1'),
        (2, 'option2'),
        (3, 'option3'),
        (4, 'option4'),
    )
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=1000)
    option = models.IntegerField(choices=options ,default=1) #select option
    
    def __str__(self):
        return self.feedback

class QuizTakers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

        
class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answered = models.BooleanField(default=False)
    user = models.ForeignKey(QuizTakers, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.user.username

    @receiver(post_save, sender=Quiz)
    def set_default_quiz(sender, instance, created,**kwargs):
        quiz = Quiz.objects.filter(id = instance.id)
        number = Question.objects.filter(quiz=instance.pk).count()
        quiz.update(question_count=number)
    @receiver(post_save, sender=Question)
    def set_default(sender, instance, created,**kwargs):
        quiz = Quiz.objects.filter(id = instance.quiz.id)
        number = Question.objects.filter(quiz=instance.quiz.pk).count()
        quiz.update(question_count= number)
    @receiver(pre_save, sender=Quiz)
    def slugify_title(sender, instance, *args, **kwargs):
        instance.slug = slugify(instance.name)
    @receiver(post_save, sender=Course_Description)
    def set_order(sender, instance, created,**kwargs):
        if not instance.ordering:
            number = Course_Description.objects.all().count()
            instance.ordering=number
            instance.save()