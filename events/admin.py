from django.contrib import admin
from events import models


class EventInstanceInline(admin.TabularInline):
    model = models.Review
    extra = 0
    readonly_fields = ['id', 'user', 'rate', 'text', 'created', 'updated', ]
    fields = ['id', 'user', 'rate', 'text', 'created', 'updated', ]
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'display_event_count', ]
    list_display_links = ['id', 'title', ]


@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    list_display_links = ['id', 'title', ]


@admin.register(models.Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'created', ]
    list_display_links = ['id', 'user', 'event', ]
    list_select_related = ['user', 'event', ]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'id', ]
    list_display = ['id', 'user', 'event', 'rate', 'text', 'created', 'updated', ]
    list_display_links = ['id', 'user', 'event', ]
    list_select_related = ['user', 'event', ]
    list_filter = ['created', 'event', ]
    fields = ['created', 'updated', 'id', ]


class FullnessFilter(admin.SimpleListFilter):
    title = 'Заполненность'
    parameter_name = 'fullness_filter'

    def lookups(self, request, model_admin):
        filter_list = (
            ('0', models.Event.FULLNESS_MIN),
            ('1', models.Event.FULLNESS_MEDIUM),
            ('2', models.Event.FULLNESS_MAX),
        )
        return filter_list

    def queryset(self, request, queryset):
        events_id = []
        for event in queryset:
            if self.value() == '2' and event.participants_number == event.enrolls.count():
                events_id.append(event.id)
            elif self.value() == '1' and event.participants_number / 2 < event.enrolls.count() < event.participants_number:
                events_id.append(event.id)
            elif self.value() == '0' and event.participants_number / 2 >= event.enrolls.count():
                events_id.append(event.id)
        return queryset.filter(id__in=events_id)


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    ordering = ['date_start']
    readonly_fields = ['display_enroll_count', 'display_places_left', ]
    list_display = ['title', 'category', 'date_start', 'is_private', 'participants_number',
                    'display_enroll_count', 'display_places_left', ]
    list_display_links = ['title', ]
    list_select_related = ['category', ]
    list_filter = [FullnessFilter, 'category', 'features', ]
    search_fields = ['title', ]

    fields = ['title', 'description', 'date_start', 'participants_number', 'is_private', 'category', 'features',
              'display_enroll_count', 'display_places_left', ]
    filter_horizontal = ['features', ]
    inlines = [EventInstanceInline]
