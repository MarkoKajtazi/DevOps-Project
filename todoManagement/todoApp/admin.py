from django.contrib import admin

from todoApp.models import Task


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'due_date', 'parent', 'owner')
    exclude = ('owner', )

    def has_change_permission(self, request, obj=None):
        return obj and obj.owner == request.user

    def has_delete_permission(self, request, obj=None):
        return obj and obj.owner == request.user

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TaskAdmin, self).save_model(request, obj, form, change)

admin.site.register(Task, TaskAdmin)