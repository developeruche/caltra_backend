# Generated by Django 3.1.8 on 2021-11-12 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_controller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedAnswersImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='answers')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedQuestionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='questions')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question_category', models.ManyToManyField(related_name='feed_question_category', to='user_controller.CategoryOfInterest')),
                ('question_image', models.ManyToManyField(related_name='feed_question_image', to='feed.FeedQuestionImage')),
                ('reaction', models.ManyToManyField(related_name='feed_question_reaction', to='user_controller.UserProfile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_author', to='user_controller.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer_image', models.ManyToManyField(related_name='feed_answer_img', to='feed.FeedAnswersImage')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_to_questions', to='feed.question')),
                ('reaction', models.ManyToManyField(related_name='feed_answer_reaction', to='user_controller.UserProfile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answer_author', to='user_controller.userprofile')),
            ],
        ),
    ]
