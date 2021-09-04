from django.urls import path
from . import views
from django.views.decorators.http import require_POST


app_name = 'events'

urlpatterns = [
    path('list/', views.EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),

    path('event-create/', views.EventCreateView.as_view(), name='event_create'),
    path('event-update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('event-enroll/', require_POST(views.EventEnrollView.as_view()), name='event_enroll'),
    path('event-delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
]
