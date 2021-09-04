from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
# from django.utils.text import slugify
# from unidecode import unidecode


class Category(models.Model):
    title = models.CharField(max_length=90, default='', verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def display_event_count(self):
        return self.events.count()


class Feature(models.Model):
    title = models.CharField(max_length=200, default='', verbose_name='Название')

    class Meta:
        verbose_name = 'Свойство события'
        verbose_name_plural = 'Свойства события'

    def __str__(self):
        return self.title


class Event(models.Model):
    FULLNESS_FREE = '0'
    FULLNESS_MIDDLE = '1'
    FULLNESS_FULL = '2'

    FULLNESS_LEGEND_FREE = '<= 50%'
    FULLNESS_LEGEND_MIDDLE = '> 50%'
    FULLNESS_LEGEND_FULL = 'sold-out'

    FULLNESS_VARIANTS = (
        (FULLNESS_FREE, FULLNESS_LEGEND_FREE),
        (FULLNESS_MIDDLE, FULLNESS_LEGEND_MIDDLE),
        (FULLNESS_FULL, FULLNESS_LEGEND_FULL),
    )

    title = models.CharField(max_length=200, default='', verbose_name='Название')
    description = models.TextField(default='', verbose_name='Описание')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(verbose_name='Количество участников')
    is_private = models.BooleanField(default=False, verbose_name='Частное')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='events')
    features = models.ManyToManyField(Feature, related_name='events')
    logo = models.ImageField(upload_to='events/event', blank=True, null=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.pk)])

    def display_enroll_count(self):
        return self.enrolls.count()

    display_enroll_count.short_description = 'Количество записей'

    def display_places_left(self):
        places_left = self.participants_number - self.enrolls.count()
        if places_left == 0:
            fullness = self.FULLNESS_LEGEND_FULL
        elif self.enrolls.count() >= places_left:
            fullness = self.FULLNESS_LEGEND_MIDDLE
        else:
            fullness = self.FULLNESS_FREE
        return f'{places_left} ({fullness})'

    display_places_left.short_description = 'Осталось мест'

    @ property
    def rate(self):
        queryset_rates = self.reviews.select_related('user').values_list('rate', flat=True)
        queryset_rates_count = queryset_rates.count()
        if queryset_rates_count == 0:
            rates = 0
        else:
            rates = sum(queryset_rates) / queryset_rates_count
        return round(rates, 1)

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/svg-icon/event.svg'

    def get_update_url(self):
        return reverse('events:event_update', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('events:event_delete', args=[str(self.pk)])


class Enroll(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='enrolls')
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, related_name='enrolls')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Запись на событие'
        verbose_name_plural = 'Записи на событие'


class Review(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='reviews')
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveSmallIntegerField(null=True, verbose_name='оценка пользователя')
    text = models.TextField(max_length=1000, default='', blank=True, verbose_name='текст отзыва')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв на событие'
        verbose_name_plural = 'Отзывы на событие'
