# Generated by Django 3.2.4 on 2021-06-30 23:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Свойство события',
                'verbose_name_plural': 'Свойства события',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(default='', max_length=90, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants_number',
            field=models.PositiveSmallIntegerField(verbose_name='Количество участников'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(null=True, verbose_name='оценка пользователя')),
                ('text', models.TextField(blank=True, default='', max_length=1000, verbose_name='текст отзыва')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='events.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отзыв на событие',
                'verbose_name_plural': 'Отзывы на событие',
            },
        ),
        migrations.CreateModel(
            name='Enroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrolls', to='events.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrolls', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Запись на событие',
                'verbose_name_plural': 'Записи на событие',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='features',
            field=models.ManyToManyField(related_name='events', to='events.Feature'),
        ),
    ]
