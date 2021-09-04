from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.views.generic import ListView, UpdateView, DetailView, TemplateView, CreateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from events.models import Event, Review, Category, Feature, Enroll
import datetime
from events.forms import EventUpdateForm, EventEnrollForm, EventCreateForm


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_objects'] = Event.objects.all()
        context['category_objects'] = Category.objects.all()
        context['feature_objects'] = Feature.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-pk')


class LoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Недостаточно прав')
        return super().get(request, *args, **kwargs)


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object

        places_left = event.participants_number - event.enrolls.count()
        try:
            fullness_percent = int(event.enrolls.count() * 100 / event.participants_number)
        except ZeroDivisionError:
            fullness_percent = 0

        context['event'] = event
        context['places_left'] = places_left
        context['fullness_percent'] = fullness_percent
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'events/event_update.html'

    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        messages.success(self.request, 'Новое событие создано успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class EventEnrollView(LoginRequiredMixin, CreateView):
    model = Enroll
    form_class = EventEnrollForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_valid(self, form):
        new_enroll = Enroll(
            user=self.request.user,
            event=self.object,
            created=datetime.date.today()

        )
        new_enroll.save()
        messages.success(self.request, f'Запись добавлена')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Вы уже записаны на это событие')
        event = form.cleaned_data.get('event', None)
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventUpdateForm

    def get_context_data(self, **kwargs):
        event = self.object
        context = super().get_context_data(**kwargs)
        context['enroll_list'] = event.enrolls.all()

        review_users = []
        review_list = event.reviews.all()
        for review in review_list:
            review_users.append(review.user)
        context['review_user_list'] = review_users
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Cобытие {form.cleaned_data["title"]} успешно изменено')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_update.html'
    success_url = reverse_lazy('events:event_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Событие {self.object} удалено')
        return result


@require_POST
def create_review(request):
    data = {
        'ok': True,
        'msg': '',
        'rate': request.POST.get('rate'),
        'text': request.POST.get('text'),
        'created': datetime.date.today(),
        'user_name': ''
    }

    try:
        event = Event.objects.get(pk=request.POST.get('event_id'))
    except ObjectDoesNotExist:
        data['msg'] = 'Событие не найдено'
        data['ok'] = False
        return JsonResponse(data)

    if not request.user.is_authenticated:
        data['msg'] = 'Отзывы могут оставлять только зарегистрированные пользователи'
        data['ok'] = False
        return JsonResponse(data)

    data['user_name'] = request.user.__str__()

    if Review.objects.filter(user=request.user, event=event).count() != 0:
        data['msg'] = 'Вы уже оставляли отзыв к этому событию'
        data['ok'] = False

    elif data['rate'] == 0 or data['text'] == '':
        data['msg'] = 'Оценка и текст отзыва - обязательные поля'
        data['ok'] = False

    else:
        new_review = Review(
            user=request.user,
            event=event,
            rate=data['rate'],
            text=data['text'],
            created=data['created'],
            updated=data['created']
        )
        new_review.save()

    return JsonResponse(data)
