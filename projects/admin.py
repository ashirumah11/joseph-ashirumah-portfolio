from django.contrib import admin
from .models import ProjectTechnology, Project


@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'badge_style', 'project_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = "Associated Projects"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'featured',
        'is_published',
        'display_order',
        'date_created',
        'has_github',
        'has_live',
    )
    list_filter = ('featured', 'is_published', 'technologies', 'date_created')
    search_fields = ('title', 'short_description', 'problem_statement', 'solution_statement')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'is_published', 'display_order')
    filter_horizontal = ('technologies',)

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "short_description", "display_order", "featured", "is_published")
        }),
        ("Engineering Case Study Details", {
            "fields": (
                "problem_statement",
                "solution_statement",
                "architecture_description",
                "key_features",
                "challenges_and_learnings",
            )
        }),
        ("Tech Stack & Media", {
            "fields": ("technologies", "image")
        }),
        ("External Links", {
            "fields": ("github_url", "live_url")
        }),
    )

    def has_github(self, obj):
        return bool(obj.github_url)
    has_github.boolean = True
    has_github.short_description = "GitHub"

    def has_live(self, obj):
        return bool(obj.live_url)
    has_live.boolean = True
    has_live.short_description = "Live Demo"
