from django.shortcuts import render 
from .form import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required , user_passes_test
from djangorave.models import PaymentTypeModel
from datetime import timedelta
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.db.models import Q
from django.template import RequestContext
#from PyPDF2 import PdfFileReader
from PIL import Image
from django.core.files import File 
from school.models import get_mime
from django.core.mail import mail_admins
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import Group
from decouple import config
from django.utils import timezone
from django.views.generic import TemplateView
from django.core.paginator import Paginator,EmptyPage , PageNotAnInteger
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rave_python import Rave,RaveExceptions
from django.core import serializers
from random import choice
rave = Rave(config('RAVE_SANDBOX_PUBLIC_KEY'), config('RAVE_SANDBOX_SECRET_KEY'), usingEnv = False)
#rave = Rave(config('RAVE_PRODUCTION_PUBLIC_KEY'),'RAVE_SECRET_KEY', production=True)


def home(request):
    authors  =  Tutor.objects.all()
  
    context = {
        'authors':authors
    }
    return render(request, 'school/index.html',context)


def prem(request):
    authors  =  Tutor.objects.all()
    message = 'Subscribe As Premium User To Access'
  
    context = {
        'authors':authors,
        'message':message
    }
    return render(request, 'school/index.html',context)


def about(request):
    return render(request, "school/about.html")

def join_course(request):
    return render(request, "school/about.html")

def gallary(request):

    return render(request, "school/gallery.html")



def index(request,error=None):
    authors  =  Profile.objects.all()
   
    context = {
        'authors':authors,
        'error':error
    }
    return render(request, "school/index.html",context)


def contact(request):

    return render(request, "school/contact.html")

def courses(request):
    course = Course_Description.objects.all()

    context = {
       
        'course': course
    }
    return render(request, "school/courses.html", context)




def is_tutor(user):
    return user.groups.filter(name='Tutor').exists()

def is_registered(user):
    premium,_ = Premium.objects.get_or_create(user=user)
    is_premium = premium.premium
    expiry = premium.expiry_date
    if timezone.now() > expiry:
        premium.premium = False
        premium.save()

    return is_premium

   
 
def loginv(request):
    form = Login()
    error = None

    if request.user is not None and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                message = 'Logged in'
                authors  =  Profile.objects.all()
                context = {
                    'message':message,
                    'author':authors
                }
                return render(request, 'school/index.html', context) 

            else:
                error='Please enter valid Username and Password.'
        
    context={
            'message':error,
            'form':form,
            'error': error
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
            authors  =  Profile.objects.all()
  
            context = {
                    'authors':authors,
                     'message' : 'Registered'
                }
            
            return render(request, 'school/index.html', context) 
        errors = form.errors
    form = SignUpForm() 
    context = {
        'form':form,
        'errors': errors
    }  
   
    return render(request,"school/register.html",context)






@login_required(login_url='login')
def update_pic(request):
    if request.POST:
        form = EditProfileImageForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render (request, 'profile.html',{'form': form})
        form = EditProfileImageForm(request.FILES)
    return render(request, 'profile.html',{'form':form})



    
            
# Add course to user's registered courses
@login_required(login_url='login')
def join(request,course_page):
    course = get_object_or_404(Course_Description, course_page)
    request.user.registered_courses.add(course)
    request.user.save()
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
        authors  =  Profile.objects.all()
  
        context = {
                    'authors':authors,
                     'message': 'Course Does Not Exist'
                }
        
         
        return render(request, 'school/index.html', context)
    listy  = subscriped.coursess.values()
    exist = False
    for i in listy:
        if i['id'] == d:
            exist = True
            continue
    
    if exist == True:
        course = get_object_or_404(Course_Description, id = course_page)
        if course.course_category.category:
            categories = course.course_category.category
        else:
            categories ='Hacking'
        course_cat =  Course_Description.objects.filter(course_category__category=categories)
   
        if request.is_ajax():
            #print('hey')
            return course_page
        sel_course = Select_course.objects.all()[:5]
        name = course.course_name
        image = Cimage.objects.filter(name=name).first()
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
                'course': course_cat, 
           
                
                
            }

        return render(request, 'school/singlecourse.html', context)
    else:
        authors  =  Profile.objects.all()
  
        context = {
                    'authors':authors,
                     'message': 'You are Not registered for this course'
                }
        
        return render(request, 'school/index.html',context)
    return HttpResponseRedirect(reverse('join_course'))




def logout_request(request):
   
    logout(request)
    authors  =  Profile.objects.all()
  
    context = {
                    'authors':authors,
                     'message': 'Logged Out'
                }
        
    return render(request, 'school/index.html',context)

def profile_view(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return HttpResponseRedirect('404')
    
    favorite = profile.favorite.values

    
    context = {
        'profile':profile,
        'favorite':favorite
    }


    return render(request, 'school/Profile.html', context)





@login_required(login_url='login')
@user_passes_test(is_registered , login_url='pay')
def compiler(request):
    RUN_URL = "https://api.hackerearth.com/v3/code/run/"
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
    if request.method == 'GET':
        return render(request, 'school/ola.html')
    else:
        return HttpResponseForbidden()
    





@login_required(login_url='login')
@user_passes_test(is_tutor, login_url='courses')
def tutorial(request):
    error = None
    if request.POST:
        course_name = int(request.POST.get('course_name'))#
        course =  get_object_or_404(Select_course,id=course_name)
        ok,_ =  Course_Description.objects.get_or_create(course_name=course)
        form = Tutorial(request.POST, user= request.user, instance= ok)
        if form.is_valid():
            ola= form.save(commit=False)
            try:
                tutor = Tutor.objects.get(user = request.user)
            except Tutor.DoesNotExist:
                tutor= Tutor.objects.create(user = request.user)
            #ola.description = 
            ola.tutor = tutor
            ola.save()
            authors  =  Profile.objects.all()
  
            context = {
                    'authors':authors,
                    'message': 'You Have just created a Topic'
                }
        
            return render(request, 'school/index.html',context)
            
        error = form.errors
    if request.is_ajax() and request.GET:
        data = int(request.GET['data'])
        sel = get_object_or_404(Select_course, id=data)
        try:
            description = Course_Description.objects.get(course_name=sel)
            if description.tutor != request.user.tutor:
                return HttpResponseForbidden()

            response = description.description
        except Course_Description.DoesNotExist:
            response = 'Nothing here ..'
        
        return JsonResponse({'response':response}, safe=False)

    form = Tutorial(user = request.user)
    context = {
        'form':form,
        'error':error
        #'name':name
    }
    return render(request, 'school/tutorial.html',context)

    
@login_required(login_url='login')    
@user_passes_test(is_tutor, login_url='courses')
def tut(request):
    if request.POST:
        form =  TutCourse(request.POST)
        if form.is_valid():
            name = request.POST.get('sel')
            ola = Select_course.objects.create(sel = name)
            ola.users.add(request.user)
            return HttpResponseRedirect(reverse('tut'))

    form = TutCourse()
    context = {
        'name':form
    }
    return render(request, 'school/tutorialname.html',context)




def pagination(request, book , page):
    page_number = request.GET.get('page',1)
    paginator = Paginator(book, per_page=page)
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books =  paginator.page(1)
    return books

def display_course(request):
    course = Course_Description.objects.all()
    images =  Cimage.objects.all()
    course  = pagination(request, course , 9)
    if request.POST:
    
        form = Search(request.POST)
        if form.is_valid():
            name =  form.cleaned_data['bar']
            ola = Course_Description.objects.filter(course_name__sel__icontains = name)
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
@user_passes_test(is_registered , login_url='prem')
def premium(request, course_page):
    ok = []
    course = get_object_or_404(Course_Description, id = course_page)
    sel_course = Select_course.objects.all()[:5]
    
    if course.course_category.category:
        categories = course.course_category.category
    else:
        categories ='Hacking'
    name = course.course_name
    course_cat =  Course_Description.objects.filter(course_category__category=categories)
   
    image = Cimage.objects.filter(name=name).first()
    description = course.description
    ola = request.user.registered_courses.values()
    name = course.course_name.sel
    for i in ola:
        ok.append(i['sel'])

        #descriptions = pagination(request, description, 3)
    context  = {
                'course': course_cat,               
                'description': description,
                'courses': sel_course,
                'image':image,
                'next': course,
                'ok':ok,
                'name':name,
                'coursepage':course,
                
            }

    return render(request, 'school/singlecourse.html', context)

@login_required(login_url='login')
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
            authors  =  Profile.objects.all()
  
            context = {
                    'authors':authors,
                     'message': 'Feedback Sent'
                }
        
            return render(request, 'school/index.html',context)            
           
        error = f.errors
    context = {
        'error':error
    }
        
    return render(request, 'school/contact.html' ,context)



def handler404(request,exception, template_name="school/404.html"):
    response = render(request,template_name)
    response.status_code = 404
    return response

def handler500(request, template_name="school/500.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response


@login_required(login_url='login')
def payment(request):
    error = None
    ola = request.user
    form = None
    olah = PaymentTypeModel.objects.filter(
            payment_plan__isnull=False
        )
    premium,_ = Premium.objects.get_or_create(user=request.user)
    if premium.premium == True:
        return HttpResponseRedirect('user_profile')
    elif not ola.email or not ola.first_name or not ola.last_name :
        olah= None
        form = PaymentForm()
    if request.POST:  
        form = PaymentForm(request.POST) 
        if form.is_valid():
            first_name =  form.cleaned_data.get('Name')
            last_name =  form.cleaned_data.get('LastName')
            ola = request.user
            ola.first_name = first_name
            ola.last_name = last_name
            if not request.user.email :
                if form.clean_email :
                    email = form.cleaned_data.get('email')
                    ola.email = email
            ola.save()
            return HttpResponseRedirect(reverse('pay'))

        error = form.errors
    

    
    context = {
        'error':error,
        'form':form,
        'pro_plan':olah
    }
    return render(request,'school/pay.html',context)
@login_required(login_url='login')
def profile(request):
    Profile,_ = Premium.objects.get_or_create(user=request.user)
    
   
    
    context = {
        
        'user_subscription': Profile,

    }
    return render(request, 'school/user.html',context)


    







@login_required(login_url='login')
def cancelSubscription(request):
    p = {
        'returnedData': {'status':None}
    }
    user_sub,_ = Premium.objects.get_or_create(user= request.user)

    if user_sub.premium is False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #vulnerable
    if request.POST:
        form = Cancel(request.POST or None)
        email =None
        if form.is_valid():
            email = form.cleaned_data.get('email')
        message =  f'Enter Your Email Address'
        if request.user.email == email:
            try:
                r2  = rave.Subscriptions.fetch(subscription_email=email)
                sub_id = r2['returnedData']['data']['plansubscriptions'][0]['id']
                p = rave.Subscriptions.cancel(sub_id) #not working
            except RaveExceptions.PlanStatusError as e:
                print(e.err)
            if p['returnedData']['status'] == 'success':
                message =  f'Your Subscription canceled {request.user.username}'
        authors  =  Profile.objects.all()
  
        context = {
                    'authors':authors,
                     'message':message
                }
        
        return render(request, 'school/index.html',context)
        

    
    return render(request, 'school/password_reset.html', {'cancel': Cancel()})
    
'''

from rave_python import Rave, Misc, RaveExceptions
rave = Rave("YOUR_PUBLIC_KEY", "YOUR_PRIVATE_KEY", usingEnv = False)
try:
   
    res = rave.Subscriptions.all()
    res = rave.Subscriptions.fetch(880)
    res = rave.Subscriptions.cancel(880)
    print(res)

except RaveExceptions.PlanStatusError as e:
    print(e.err)

except RaveExceptions.ServerError as e:
    print(e.err)
'''
@login_required(login_url='login')
def callback(request,reference,amount ):
    res = {
        'status':False
    }
    
    try:
        res = rave.Account.verify(reference)
    except RaveExceptions.TransactionVerificationError as e:
        return HttpResponseRedirect(reverse('user_profile'))
    try:
        res = rave.Card.verify(reference)
    except RaveExceptions.TransactionVerificationError as e:
        return HttpResponseRedirect(reverse('user_profile'))
    
    if res['vbvmessage'] == 'Approved. Successful':
        if res['chargecode'] == '00':
            if amount == res['amount']:
                premium,_ = Premium.objects.get_or_create(user=request.user)
                payment = PaymentTypeModel.objects.get(amount=amount)
                expiry  = payment.expiry
                premium.expiry_date = timezone.now().date()+timedelta(days=expiry)
                premium.premium =True
                premium.save()
                return HttpResponseRedirect(reverse('user_profile'))
        
    return render(request, 'school/index.html')
          

@login_required(login_url='login')
def take_quiz(request,topic):
    #register Quiz, who is the quiztaker?
    course = get_object_or_404(Course_Description, pk=topic)
    if course.premium and request.user.premium.premium == False:
        #quiz is for premium user redirect
        return False, False
    quiz = get_object_or_404(Quiz, topic=course)
    taker,_ = QuizTakers.objects.get_or_create(user= request.user, quiz =quiz)
    return quiz, taker

@login_required(login_url='login')
def quiz_score(request,topic):
    course = get_object_or_404(Course_Description, pk=topic)
    quiz = get_object_or_404(Quiz, topic=course)
    taker = get_object_or_404(QuizTakers, quiz = quiz , user=request.user)
    context ={
        'topic': topic,
    }
    count =  Response.objects.filter(user=taker, question__quiz=quiz,answered=True).count()  
        
    if quiz.question_count == count :
            taker.completed = True
            
    else:
        taker.completed = False

    taker.save()

    if taker.completed:
        try:
            score  = taker.correct_answers/ quiz.question_count * 100
        except ZeroDivisionError:
            score = 0
    else:
        try:
            #find unanswered questions on the topic
            question = Response.objects.filter(user=taker,question__quiz=quiz, answered=False).first().question
            questions = list(Question.objects.filter(quiz=quiz))
            number = questions.index(question)
            context['question']=question
        except AttributeError:
            course = Course_Description.objects.all()[:5]

            context = {
                
                    'course': course
                }
            return render(request, 'school/courses.html',context)
        context['answered'] = False
        context['now'] = number
        context['next'] = number+1
        return render(request, 'school/quiz.html',context)

    context['score'] = score
    
    return render(request , 'school/score.html', context)
   

@login_required(login_url='login')

def question(request,topic,question):
    quiz,taker = take_quiz(request, topic)
   #check if there is a quiz on the course 
    if quiz and taker is False:
        authors  =  Profile.objects.all()
        context = {
                    'authors':authors,
                    'message': 'Topic is for premium users only'
                 }
        return render(request , 'school/index.html',context)
    questions = Question.objects.filter(quiz=quiz)

    
    if request.is_ajax() and request.GET:
        try:
            answer = int(request.GET['data'])
        except MultiValueDictKeyError:
            return HttpResponseRedirect(reverse('question'))
        number  = len(questions)
        if question <= number :
            Questin_sent = questions[question]
            response,_ =Response.objects.get_or_create(user=taker, question=Questin_sent)
            
        else:
            return HttpResponseRedirect(reverse('index'))


        answer_q = get_object_or_404(Answer, question = Questin_sent)
        if answer == answer_q.option and not response.answered:
            taker.correct_answers = taker.correct_answers+1
            
        if not response.answered:
            response.answered = True
            response.save()

        count =  Response.objects.filter(user= taker, question__quiz=quiz,answered=True).count()  
        
       
        if quiz.question_count == count :
            taker.completed = True
            #redirect to score page
            #return HttpResponseRedirect(reverse('quiz', args=(topic, )))
        else:
            taker.completed = False
    

        taker.save()    # return to score page

        answer = serializers.serialize('json', [answer_q, ])

        
        return JsonResponse(answer, safe=False)

    
    number  = len(questions)
    #print(number)
    try:
        question_to_send = questions[question]
        next_question = question+1

    except IndexError:#redirect to score
        return HttpResponseRedirect(reverse('quiz', args=(topic, )))
     
    try:
        response,_ =Response.objects.get_or_create(user=taker, question=question_to_send)
        respon = response.answered
    except Response.DoesNotExist:
        respon = False

    context ={
        'question':question_to_send,
        'topic': topic,
        'next' : next_question,
        'now':question,
        'answered': respon
    }
    return render(request, 'school/quiz.html',context)

    


    

    
    

    
@login_required(login_url='login')
@user_passes_test(is_tutor, login_url='courses')
def create_quiz(request):
    question_created = None
    if request.POST:
        form =  QuestionForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            course = get_object_or_404(Course_Description, id=course)
            quiz_description = form.cleaned_data.get('quiz_description')
            question = form.cleaned_data.get('question')
            option1 = form.cleaned_data.get('option1')
            option2 = form.cleaned_data.get('option2')
            option3 = form.cleaned_data.get('option3') #check cleaned data
            option4 = form.cleaned_data.get('option4')
            answer = form.cleaned_data.get('answer')
            feedback = form.cleaned_data.get('feedback')
            name = course.course_name.sel
            quiz, _ = Quiz.objects.get_or_create(topic=course)
            if _ is True:
                quiz.name= name
                quiz.description= quiz_description
                quiz.save()
            created  = Question.objects.create(
                quiz = quiz,
                question_asked = question,
                option1 = option1,
                option2 = option2,
                option3 = option3,
                option4 = option4
            )
            Answer.objects.create(
                question = created,
                feedback = feedback,
                option = answer

            )
            question_created = 'Question Added add another'



    form = QuestionForm()
    context ={
        'form':form,
        'quest':question_created
    }
    return render(request, 'school/quizpage.html', context)
    
 
@login_required(login_url='login')
@user_passes_test(is_tutor, login_url='courses')
def display_questions(request):
    questions = Question.objects.all().order_by('quiz__topic')
    context = {
        'question': questions
    }

    return render(request, 'school/quizdisplay.html', context)    
    
@login_required(login_url='login')
@user_passes_test(is_tutor, login_url='courses')
def edit_quiz(request, edit_or_del, num):

    if edit_or_del == 'edit':
        o  =  get_object_or_404(Question, id=num)
        topic = o.quiz.topic
        options = list(o.answer.options)
        instance ={
            'course' : (topic.id,topic.course_name) ,
            'quiz_description' : o.quiz.description ,
            'question' : o.question_asked ,
            'option1' : o.option1 ,
            'option2' : o.option2,
            'option3' : o.option3,
            'option4' : o.option4,
            'answer' : options[o.answer.option],
            'feedback' : o.answer.feedback
        }
        form  =  QuestionForm(initial=instance)
        
        question_created = None
        context ={
        'form':form,
        'quest':question_created
        }
        return render(request, 'school/quizpage.html', context)


    if edit_or_del == 'delete':
        question =get_object_or_404(Question, id=num)
        if question.quiz.topic.tutor == request.user.tutor:

            question.delete()
            
        else:
            return HttpResponseForbidden()


    return HttpResponseRedirect(reverse('all_questions'))