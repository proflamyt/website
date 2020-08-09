from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home , name="home"),
    path('about', views.about, name='about'),
    path('join/<int:course_page>', views.join, name='join'),
    path('register', views.register, name='register'),
    path("index", views.index, name='index'),
    path("login", views.loginv, name="login"),
    path("gallary", views.gallary, name='gallary'),
    path("contact",views.contact,name='contact'),
    path('register', views.register, name='register'),
    path("courses",views.courses,name='courses'),
    path("upload", views.upload_book , name='upload'),
    path("join_course", views.join_course , name='join_course'),
    path("download", views.download, name='download'),
    path("<int:book_id>", views.about_books, name='about_books'),
    path("logout", views.logout_request , name='logout'),
    path("profile", views.profile_view, name='profile'),
    path("edit",views.update_pofile, name = 'edit'),
    path('ratings', include('star_ratings.urls', namespace='ratings'), name='ratings'),
    path("author",views.reg_author, name = 'author'),
    path("run/",views.compiler, name = 'run'),
    path('<int:downloadfile>/', views.download_file , name='file'),
    path("display",views.display_course, name = 'display'),
    path("tutname",views.tut, name = 'tutname'),
    path("tut",views.tutorial, name = 'tut'),
    path("genre/<int:id>",views.genre_func, name = 'genre'),
    path("feedback",views.mail, name = 'feedback'),
    path("premium/<int:course_page>",views.premium, name = 'premium'),
    path('accounts/', include('allauth.urls')),
  
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='school/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='school/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='school/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='school/password_reset_done.html'), name='password_reset_complete'),



]