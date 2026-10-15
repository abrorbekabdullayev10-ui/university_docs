from django.contrib import admin
from .models import Direction, Group

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'year')
    list_filter = ('direction', 'year')
    search_fields = ('name',)
    ordering = ('-year', 'name')