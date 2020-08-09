from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
import magic
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
import sys
from phonenumber_field.modelfields import PhoneNumberField
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.core.exceptions  import ValidationError
valid_file = FileExtensionValidator (allowed_extensions=['pdf', 'doc', 'epub' ])
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
    if 'pdf'or 'html'or 'epub' in mimetype : 
        return value
    else:
        return ValidationError('This Field accept only book format')



# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}"

class Novel(models.Model):
     title = models.CharField(max_length=200,blank=True, null=True)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
     author = models.ForeignKey('Profile', on_delete=models.SET_NULL,blank=True, null=True)
    
    
     summary = RichTextField()

     isbn = models.CharField( max_length=13, null=True, blank=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn"> ISBN number </a>')
    
    # ManyToManyField used because genre can contain many books. EBooks can cover many genres.
    # Genre class has already been defined so we can specify the object above.
     genre = models.ManyToManyField(Genre, help_text='Select multiple genres for this book')
     
     bookFile = models.FileField(blank=False,upload_to='book_files/' , validators= [valid_file,valid_pdf_mimetype,valid_size])
     
     date_uploaded = models.DateTimeField(default = timezone.now)

     bookImage = models.ImageField(default ='default_profile.jpg', upload_to='book/images/', validators= [valid_image,valid_image_mimetype,valid_size]) 
     
     created_author = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
     
     ratings = GenericRelation(Rating, related_query_name='novels')


    
  

     def save(self, *args, **kwargs):
         
        self.bookImage = self.compress(self.bookImage)
        super(Novel, self).save( *args,**kwargs )

     def compress (self, bookImage):
        im = Image.open(bookImage)
        im_io = BytesIO()
        im = im.resize((480,380 ))
        im = im.convert('RGB')
        im.save(im_io, 'JPEG', quality=90)
        im_io.seek(0)
        bookImage = InMemoryUploadedFile(im_io,'ImageField', '%s.jpg' % bookImage.name.split('.')[0], 'image/jpeg',sys.getsizeof(im_io), None)
        return bookImage
        
     def __str__(self):
        return f"{self.title}"



class Profile(models.Model):
    authorName = models.CharField(max_length=200)

    user = models.OneToOneField(User, on_delete=models.CASCADE) 

    favorite = models.ManyToManyField('Novel',blank=True)
    
    profile_image = models.ImageField(default ='default_profile.jpg', upload_to='profile/images' , validators = [valid_image,valid_image_mimetype,valid_size])   

    about_me = models.TextField(blank=True, null=True)

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
    course_category  = models.ForeignKey('Course_category',  on_delete=models.SET_NULL, null=True)
    course_name = models.OneToOneField('Select_course', on_delete= models.CASCADE,blank=True, null=True ,related_name='description')
    premium = models.BooleanField( default= False)
    description = RichTextUploadingField()
    tutor =  models.ForeignKey('Tutor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.course_name}"

class Course_category(models.Model):
    category = models.TextField(max_length=15)

    def __str__(self):
        return f"{self.category}"


class Cimage(models.Model):
    course_image = models.ImageField(upload_to='course/images' ,  validators = [valid_size, valid_image,valid_image_mimetype])
    name =  models.ForeignKey('Select_course', on_delete= models.CASCADE,blank=True, null=True ,related_name='image')
    title = models.CharField(max_length = 14)

    def save(self, *args, **kwargs):
        if not self.id:
            self.course_image = self.compress(self.course_image)
        super(Cimage, self).save(*args,**kwargs)
    def compress(self, image):
        im = Image.open(image)
        im_io = BytesIO()
        im = im.resize(( 300 ,416))
        im = im.convert('RGB')
        im.save(im_io, 'JPEG', quality=90)
        im_io.seek(0)
        profile_image = InMemoryUploadedFile(im_io,'ImageField', '%s.jpg' % image.name.split('.')[0], 'image/jpeg',sys.getsizeof(im_io), None)
        return profile_image
        
    def __str__(self):
        return f"{self.title}"
    
class Course(models.Model):
    name = models.CharField(max_length=30,blank=True, null=True)
    gender = models.CharField(max_length=6,blank=True, null=True)
    Email = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True ,related_name='course_name')
    Phone = PhoneNumberField('INTERNATIONAL')
    coursess =models.ManyToManyField(Course_category, blank=True, related_name='course_sel')
    #courseb = models.ManyToManyField(Course_category, blank=True)
    category1 = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.name}"

class Select_course(models.Model):
    sel = models.CharField(max_length=200, help_text='Write the topics you want to')
    users = models.ManyToManyField(User, blank=True, related_name='registered_courses')
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.sel}"

class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}"

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE,blank=True, null=True ,related_name='tutor')
    image = models.ImageField(default ='default_profile.jpg', upload_to='book/tutors/', validators= [valid_image,valid_image_mimetype,valid_size]) 
    instagram = models.CharField(max_length=30, null=True)
    twitter = models.CharField(max_length=30, null=True)
    github = models.CharField(max_length=30, null=True)
    def save(self, *args, **kwargs):
         if not self.id:
            self.mage = self.compress(self.image)
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
