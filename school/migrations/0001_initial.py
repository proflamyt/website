# Generated by Django 4.0.1 on 2022-02-16 22:47

import ckeditor_uploader.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import school.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('subscribed', models.BooleanField(default=False)),
                ('is_tutor', models.BooleanField(default=False)),
                ('Phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='INTERNATIONAL')),
                ('gender', models.CharField(choices=[('1', 'Male'), ('0', 'Female')], max_length=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default_profile.jpg', upload_to='courses/images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg']), school.models.valid_image_mimetype, school.models.valid_size])),
                ('premium', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course_Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, unique=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('ordering', models.IntegerField(blank=True, null=True, unique=True)),
                ('course_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.course_category')),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_asked', models.CharField(blank=True, default='ola', max_length=1000, null=True)),
                ('option1', models.CharField(blank=True, default='ola', max_length=100, null=True)),
                ('option2', models.CharField(blank=True, default='ola', max_length=100, null=True)),
                ('option3', models.CharField(blank=True, default='ola', max_length=100, null=True)),
                ('option4', models.CharField(blank=True, default='ola', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('question_count', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=70)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField()),
                ('roll_out', models.BooleanField(default=False)),
                ('topic', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.course_description')),
            ],
            options={
                'verbose_name_plural': 'Quizzes',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='QuizTakers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default_profile.jpg', upload_to='book/tutors/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg']), school.models.valid_image_mimetype, school.models.valid_size])),
                ('instagram', models.CharField(max_length=30, null=True)),
                ('twitter', models.CharField(max_length=30, null=True)),
                ('github', models.CharField(max_length=30, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Select_course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sel', models.CharField(help_text='Write the topics you want to', max_length=200, unique=True)),
                ('users', models.ManyToManyField(blank=True, related_name='registered_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.quiztakers')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.quiz'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorName', models.CharField(max_length=200)),
                ('profile_image', models.ImageField(default='default_profile.jpg', upload_to='profile/images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg']), school.models.valid_image_mimetype, school.models.valid_size])),
                ('about_me', models.TextField(blank=True, null=True)),
                ('instagram', models.CharField(max_length=30, null=True)),
                ('twitter', models.CharField(max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiry_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course_description',
            name='course_name',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='description', to='school.select_course'),
        ),
        migrations.AddField(
            model_name='course_description',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.tutor'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=1000)),
                ('option', models.IntegerField(choices=[(1, 'option1'), (2, 'option2'), (3, 'option3'), (4, 'option4')], default=1)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='school.question')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='registered_courses',
            field=models.ManyToManyField(to='school.Course_Description'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
