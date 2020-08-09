from django.shortcuts import render 
from .form import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required , user_passes_test
# Create your views here.
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from PyPDF2 import PdfFileReader
from PIL import Image
from django.core.files import File 
from school.models import get_mime
from django.core.mail import mail_admins

from django.http import HttpResponse
from django.contrib.auth.models import Group
from decouple import config
from django.core.paginator import Paginator,EmptyPage , PageNotAnInteger
 

RUN_URL = "https://api.hackerearth.com/v3/code/run/"

def home(request):
    authors  =  Profile.objects.all()
  
    context = {
        'authors':authors
    }
    return render(request, 'school/index.html',context)

def about(request):

    return render(request, "school/about.html")





def gallary(request):

    return render(request, "school/gallery.html")



def index(request):
    authors  =  Profile.objects.all()
   
    context = {
        'authors':authors
    }
    return render(request, "school/index.html",context)
def contact(request):

    return render(request, "school/contact.html")

def courses(request):
    images = Cimage.objects.all()[:4]
    course = Course_Description.objects.all()[:5]

    context = {
        'image':images,
        'course': course
    }
    return render(request, "school/courses.html", context)


def is_author(user):
    return user.groups.filter(name='Author').exists()

def is_tutor(user):
    return user.groups.filter(name='Tutor').exists()
def is_registered(user):
    return user.groups.filter(name="Premium").exists()

   
 
def loginv(request):
    form = Login()
    error = None

    if request.user is not None and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
       
        if user is not None:
            
            login(request, user)
            message = 'Logged in'
            return render(request, 'school/index.html', {'message':message}) 

        else:
            error='Please enter valid Username and Password.'
    context={
            'message':error,
            'form':form
        }       
    return render(request, 'school/login.html',context)

        

   



def register(request):

 #   if request.user is not None and request.user.is_authenticated:
 #       return render(request,"school/index.html")
    errors = None
    if request.method =='POST':
        form = SignUpForm(request.POST)
      
        
        if form.is_valid() and form.clean_email() and form.clean_password():
            ola = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            
            login(request, user)
            message = 'Registered'
            return render(request, 'school/index.html', {'message':message}) 
        errors = form.errors
    form = SignUpForm() 
    context = {
        'form':form,
        'errors': errors
    }  
   
    return render(request,"school/register.html",context)

@login_required(login_url='login')
def upload_book(request):
    error = None

    if request.method == 'POST':
        book_form = UploadBookForm(request.POST, request.FILES, instance = request.user)
     
        if book_form.is_valid():
            title = request.POST.get('title')        
            summary = request.POST.get('summary')
            isbn = request.POST.get('isbn')
            genre = request.POST.getlist('genre')   
            bookImage = request.FILES.get('bookImage')  
            bookFile = request.FILES.get('bookFile')
            book = Novel.objects.create()
            for i in range(len(genre)):
                book.genre.add(genre[i])   
            book.title=title
            book.summary=summary
            book.isbn=isbn
            book.bookFile = bookFile
            book.created_author= request.user
            if bookImage:
                book.bookImage= bookImage    
            try:
                author =  Profile.objects.get(user = request.user )
            except Profile.DoesNotExist:
                author = Profile(authorName = request.user.username, user = request.user)
                author.save()
            book.author = author
            book.save()
            author_group = Group.objects.get(name='Author')
            author_group.user_set.add(request.user)
            
             
            message = 'Book Uploaded'
            return render(request, 'school/index.html', {'message':message}) 
        error = book_form.errors
    book_form = UploadBookForm(request.POST,request.FILES, instance = request.user)
    context = {
            'error':error,
            'book_form': book_form

        }
        
        
    return render(request,'school/upload.html', context)



@login_required(login_url='login')
def update_pofile(request):
    if request.POST:
        instance = Profile.objects.get(user=request.user)
        form = EditProfileForm(request.POST , request.FILES , user= request.user, instance=instance)
  
        if form.is_valid():
          


            form.save()

            return render(request,'school/index.html')
  
    form = EditProfileForm( user = request.user ,  instance = request.user.profile)
    
    context = {
        'profile_form' : form,
        
    }
    return render(request, 'school/edit.html',context)

@login_required(login_url='login')
def update_pic(request):
    if request.POST:
        form = EditProfileImageForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render (request, 'profile.html',{'form': form})
        form = EditProfileImageForm(request.FILES)
    return render(request, 'profile.html',{'form':form})


def download(request):
    booky = Novel.objects.all().order_by('-ratings__average')
    #this = booky.order_by('date_uploaded')
    genres =  Genre.objects.all()
    books  = pagination(request, booky , 6)
    if request.POST:
       
        form = Search(request.POST)
        if form.is_valid():
            name =  request.POST.get('bar')
           
            query = Q(author__authorName__icontains = name)
            query.add(Q(title__icontains= name),Q.OR)
            query.add(Q(genre__name__icontains= name),Q.OR)
            ola = Novel.objects.filter(query)
            olah = pagination(request ,  ola  , 9)
            form = Search()
            context={
                'form': form,
                'novel':olah,
                'top' : books,
                'name':name,
                
                'genre':genres
                
            }

            return render (request,'school/search.html',context)
    form = Search()
    context={
                'form': form,
                'top' : books,
                'genre':genres
            }
    return render(request,'school/search.html',context)

@login_required(login_url='login')
def join_course(request):
    error = None
    
    if request.POST:
        courses =request.POST.getlist('coursess')
        try:
            instance = Course.objects.get(Email=request.user)
            form = Courses(request.POST , instance= instance)
        except Course.DoesNotExist:
            form = Courses(request.POST)
            
        if form.is_valid():
            ola= form.save(commit=False)
            ola.Email = request.user
            ola.save()
            for course in courses:
                ola.coursess.add(course)
            ola.save()
     
            message = 'Course Registered'
            return render(request, 'school/index.html', {'message':message})
        error = form.errors 
    
    try:
        instance = Course.objects.get(Email=request.user)
        form = Courses(  instance = instance )
    except Course.DoesNotExist:
        form = Courses()
    
    context = {
            'error':error,
            'form':form
        }
        
        
        

    return render(request,'school/join.html',context)
            

@login_required(login_url='login')
def join(request,course_page):
    try:
        subscriped  = Course.objects.get(Email= request.user)
    except Course.DoesNotExist:
        
        return HttpResponseRedirect(reverse('join_course'))
   
    ok = []
    
    
    if request.user.registered_courses:
        olab = request.user.registered_courses.values()
        for ol in olab:
            ok.append(ol['sel'])   
    else:
        return HttpResponseRedirect(reverse('join_course')) 
    try:
        d = Course_Description.objects.get(pk = course_page)
        d = d.course_category.id
        
    except Course_Description.DoesNotExist:
        message = 'Course Does Not Exist'
        return render(request, 'school/index.html', {'message':message})
    listy  = subscriped.coursess.values()
    exist = False
    for i in listy:
        if i['id'] == d:
            exist = True
            continue
    
    if exist == True:
        course = Course_Description.objects.get(id = course_page)
        if course.course_category.category:
            categories = course.course_category.category
        else:
            categories ='Hacking'
        course_cat =  Course_Description.objects.filter(course_category__category=categories)
        sel_course = Select_course.objects.all()[:5]
        image = Cimage.objects.filter(id = course_page)
        if not course.premium:
            description = course.description
            name = course.course_name.sel
        else:
            return HttpResponseRedirect(reverse('premium', args=(course_page, )))


        context  = {
                'coursepage': course,               
                'description': description,
                'courses': sel_course,
                'image':image,
                'ok':ok,
                'name':name,
                'course': course_cat
                
                
            }

        return render(request, 'school/singlecourse.html', context)
    else:
        print(exist)
        message = 'You are Not registered for this course'
        return render(request, 'school/index.html', {'message':message})
    return HttpResponseRedirect(reverse('join_course'))

def about_books(request, book_id ):
    books = Novel.objects.get(pk=book_id)
    genres =  Genre.objects.all()
    genre1_top_books= Novel.objects.filter(genre = genres[0]).order_by('date_uploaded')[:1]
    genre2_top_books= Novel.objects.filter(genre = genres[1]).order_by('date_uploaded')[:1]
    genre3_top_books= Novel.objects.filter(genre = genres[2]).order_by('date_uploaded')[:1]
    genre4_top_books= Novel.objects.filter(genre = genres[3]).order_by('date_uploaded')[:1]
    genre5_top_books= Novel.objects.filter(genre = genres[4]).order_by('date_uploaded')[:1]
    genre6_top_books= Novel.objects.filter(genre = genres[5]).order_by('date_uploaded')[:1] 
    context= {
        'book' : books,
        'genre' : genres,
        
        
    }
    context['Horror']=genre1_top_books
    context['Satire']=genre2_top_books
    context['Action']=genre3_top_books
    context['Romance']=genre4_top_books
    context['Fantasy']=genre5_top_books
    context['Mythology']=genre6_top_books



    return render(request , 'school/single.html' , context)

def genre_func(request, id):
    genres =  Genre.objects.get(id=id)
    genre_display =  Novel.objects.filter(genre = genres ).order_by('date_uploaded')
    genre = pagination(request,genre_display,9) 
    form = Search()
    context = {
        'top':genre_display,
        'form':form,
        'genres':genres
    }
    return render(request, 'school/search.html',context)


def logout_request(request):
   
    logout(request)
    message = 'log out successful'
    return render(request,"school/index.html", {'message':message})

def profile_view(request):
    return render(request, 'school/Profile.html')





@login_required(login_url='login')
@user_passes_test(is_registered , login_url='index')
def compiler(request):
    if request.is_ajax():
        source = request.POST['source']
        lang = request.POST['lang']
        data = {
        'client_secret': config('API_KEY') ,
        'async': 0,
        'source': source,
        'lang': lang,
        'time_limit': 5,
        'memory_limit': 262144,
        }
        if 'input' in request.POST:
            data['input'] = request.POST['input']
            r = request.post(RUN_URL, data=data)		      
            return JsonResponse(r.json(), safe=False)

        else:
            return HttpResponseForbidden()
    return render(request, 'school/ola.html')




def pdf_view(book ):
  
    with open(book , 'rb') as p :
        pdf = PdfFileReader(p)
        info = pdf.getDocumentInfo()
        no_of_pages = pdf.getNumPages()
        context = {
            'pdf':pdf,
            'info':info,
            'no_of_pages':no_of_pages,
            
        }
        return context
        '''
      response = HttpResponse(pdf, mimetype= '/application/pdf')
        response['Content- Disposition'] = f'inline;filename= cHowTV{book.name}.pdf'
        pdf.close()   
'''
def pagination(request, book , page):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(book, per_page=page)
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books =  paginator.page(1)
    return books

@login_required(login_url='login')
@user_passes_test(is_author, login_url='upload') 
def reg_author(request):  
    if Profile.objects.filter(user=request.user).exists():
        return HttpResponseRedirect(reverse('edit'))
    error = None 
    search = Search()
    if request.POST:
        form = ProfileForm(request.POST,request.FILES, user= request.user)

        if form.is_valid():
            authorName = request.POST.get('authorName')        
            about_me = request.POST.get('about_me')
            favorite = request.POST.getlist('favorite')          
            profile_image = request.FILES.get('profile_image')  
            prof = Profile.objects.create(user = request.user)
            prof.user = request.user
            prof.authorName =  authorName
            
            for i in range(len(favorite)):
                prof.favorite.add(favorite[i]) 
            if profile_image:
                prof.profile_image = profile_image
            prof.about_me = about_me
            prof.save()
            form.save()

            return HttpResponseRedirect(reverse('upload'))

        error =  form.errors
    form = ProfileForm(user=request.user)
    context = {
        'form':form,
        'error': error,
        'search': search
    }
    return render(request,'school/author.html',context)
@login_required(login_url='login')
@user_passes_test(is_tutor, login_url='courses')
def tutorial(request):
    if request.POST:
        form = Tutorial(request.POST, user= request.user)
        if form.is_valid:
            ola= form.save(commit=False)
            try:
                tutor = Tutor.objects.get(user = request.user)
            except Tutor.DoesNotExist:
                tutor= Tutor.objects.create(user = request.user)
            ola.tutor = tutor
            ola.save()
            message = 'Course created'
            return render(request, 'school/index.html', {'message':message}) 

    form = Tutorial(user = request.user)
    context = {
        'form':form,
        #'name':name
    }
    return render(request, 'school/tutorial.html',context)

    
@login_required(login_url='login')    
@user_passes_test(is_tutor, login_url='courses')
def tut(request):
    if request.POST:
        form =  TutCourse(request.POST)
        if form.is_valid:
            name = request.POST.get('sel')
            ola = Select_course.objects.create(sel = name)
            ola.users.add(request.user)
            return HttpResponseRedirect(reverse('tut'))

    form = TutCourse()
    context = {
        'name':form
    }
    return render(request, 'school/tutorialname.html',context)




def download_file(request, downloadfile):
    book = Novel.objects.get(pk=downloadfile)
    fl_path = book.bookFile.path
    filename =  f'{book.title}'
    fl = open(fl_path,'rb')
    mime_type = get_mime(fl)
    if 'pdf' in mime_type:
        ola  = pdf_view(fl_path)
        if ola['no_of_pages'] < 300 or 'doc' in mime_type:
            return HttpResponseRedirect(reverse('about_books', args=(downloadfile,)))

    response = HttpResponse(fl, content_type = mime_type)
    response['Content-Disposition'] =  "attachment; filename = %s" % filename
    return response

def display_course(request):
    course = Course_Description.objects.all()
    images =  Cimage.objects.all()
    course  = pagination(request, course , 9)
    if request.POST:
    
        form = Search(request.POST)
        if form.is_valid():
            name =  request.POST.get('bar')
            ola = Course_Description.objects.filter(course_name__sel__icontains = name).order_by()
            ola = pagination(request, ola, 9)
            form = Search()
            context={
                'form': form,
                'novel':ola,
                'top' : course,
                'name':name,
                'images':images 
                
            }

            return render (request,'school/display.html',context)
    form = Search()
    context={
                'form': form,
                'top' : course
            }
    return render(request,'school/display.html',context)

  


@login_required(login_url='login')
@user_passes_test(is_registered , login_url='index')
def premium(request, course_page):
    ok = []
    course = Course_Description.objects.get(id = course_page)
    sel_course = Select_course.objects.all()[:5]
    if course.course_category.category:
        categories = course.course_category.category
    else:
        categories ='Hacking'
    course_cat =  Course_Description.objects.filter(course_category__category=categories)
    image = image = Cimage.objects.filter(id = course_page)
    description = course.description
    ola = request.user.registered_courses.values()
    for i in ola:
        ok.append(i['sel'])

        #descriptions = pagination(request, description, 3)
    context  = {
                'course': course_cat,               
                'description': description,
                'courses': sel_course,
                'image':image,
                'next': course,
                'ok':ok
                
            }

    return render(request, 'school/singlecourse.html', context)


def mail(request):
    error = None
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
 
        if f.is_valid():
            name = f.cleaned_data['name']
            sender = f.cleaned_data['email']
            subject  = f.cleaned_data['subject']
            message = f.cleaned_data['message']
            subject = f"You have a new Feedback from {name}:{sender}"
            message = f"Subject: {subject}\n\nMessage: {message}"
            mail_admins(subject, message)
 
            f.save()
            return render(request, 'school/index.html' ,{'message':'message sent'})
        error = f.errors
    context = {
        'error':error
    }
        
    return render(request, 'school/contact.html' ,context)



def handler404(request, template_name="404.html"):
    response = render(request,"404.html")
    response.status_code = 404
    return response

def handler500(request, template_name="school/500.html"):
    response = render(request, "school/500.html")
    response.status_code = 500
    return response