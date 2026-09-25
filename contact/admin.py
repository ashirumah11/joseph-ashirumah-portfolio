from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'ip_address')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'ip_address')
    ordering = ('-created_at',)
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        rows_updated = queryset.update(is_read=True)
        self.message_user(request, f"{rows_updated} message(s) marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        rows_updated = queryset.update(is_read=False)
        self.message_user(request, f"{rows_updated} message(s) marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"
