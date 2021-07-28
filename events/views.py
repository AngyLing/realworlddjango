from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from events.models import Event, Review


def event_list(request):
    template_name = 'events/event_list.html'
    return render(request, template_name)


def event_detail(request, pk):
    template_name = 'events/event_detail.html'
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
        'places_left': event.participants_number - event.display_enroll_count(),
    }
    return render(request, template_name, context)


@require_POST
def create_review(request):
    data = {
        'ok': True,
        'msg': '',
        'rate': int(request.POST.get('rate', 0) or 0),
        'text': request.POST.get('text', ''),
        'created': '',
        'user_name': request.POST.get('user_name', '')
    }

    if request.user.is_authenticated is False:
        data['msg'] = 'Отзывы могут оставлять только зарегистрированные пользователи'
        data['ok'] = False

    if data['rate'] == 0 or data['text'] == '':
        data['msg'] = 'Оценка и текст отзыва - обязательные поля'
        data['ok'] = False

    if data['user_name'] in Event.reviews.user.objects.all():
        data['msg'] = 'Вы уже оставляли отзыв к этому событию'
        data['ok'] = False

    if data['ok'] is True:
        new_review = Review()
        new_review.user = data['user_name']
        new_review.event = Event.title
        new_review.rate = data['rate']
        new_review.rate = data['text']
        new_review.save()
    return HttpResponse(data)
