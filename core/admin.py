from django.contrib import admin
from .models import (
    Profile,
    SkillCategory,
    Skill,
    Experience,
    ValuePillar,
    SocialLink,
    SiteSettings,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Personal Identity", {
            "fields": (
                "name",
                "professional_title",
                "eyebrow_text",
                "headline",
                "subheadline",
                "short_bio",
                "about_text",
            )
        }),
        ("Media & Documents", {
            "fields": ("profile_photo", "cv_file")
        }),
        ("Contact & Location", {
            "fields": ("email", "phone", "location")
        }),
        ("Status & Availability", {
            "fields": ("status_badge", "status_active")
        }),
        ("Social Profile Links", {
            "fields": ("github_url", "linkedin_url", "twitter_url")
        }),
        ("Terminal Code Snippet", {
            "fields": ("hero_code_snippet",),
            "classes": ("collapse",)
        }),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('name', 'icon_class', 'is_primary_stack', 'short_description', 'order')


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'key', 'icon', 'order', 'skill_count')
    inlines = [SkillInline]

    def skill_count(self, obj):
        return obj.skills.count()
    skill_count.short_description = "Skills Count"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_primary_stack', 'order', 'short_description')
    list_filter = ('category', 'is_primary_stack')
    search_fields = ('name', 'short_description')
    list_editable = ('order', 'is_primary_stack')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'organization',
        'experience_type',
        'start_date',
        'end_date',
        'is_current',
        'order',
    )
    list_filter = ('experience_type', 'is_current')
    search_fields = ('title', 'organization', 'description')
    list_editable = ('order',)


@admin.register(ValuePillar)
class ValuePillarAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'short_summary')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'label', 'url', 'is_active', 'order')
    list_filter = ('is_active', 'platform')
    list_editable = ('is_active', 'order')
    search_fields = ('label', 'url')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Site Metadata", {
            "fields": ("site_title", "meta_description", "footer_text")
        }),
        ("Contact Settings", {
            "fields": ("contact_email", "enable_contact_form", "enable_hire_cta")
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
