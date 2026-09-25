from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class ProjectTechnology(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    badge_style = models.CharField(
        max_length=50,
        default="badge-cyan",
        help_text="Color class, e.g. badge-cyan, badge-blue, badge-emerald, badge-purple, badge-amber"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Project Technology Tag"
        verbose_name_plural = "Project Technology Tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(
        max_length=300,
        help_text="Concise 1-2 sentence summary for project cards"
    )
    problem_statement = models.TextField(
        help_text="The real-world problem or operational bottleneck this project was engineered to solve"
    )
    solution_statement = models.TextField(
        help_text="Detailed engineering solution, user journey, and technical resolution"
    )
    architecture_description = models.TextField(
        help_text="Technical architecture, data modeling, backend services, API contracts, and integration points"
    )
    key_features = models.TextField(
        help_text="Breakdown of key capabilities, operational workflows, and security implementations"
    )
    challenges_and_learnings = models.TextField(
        help_text="Performance bottlenecks overcome, trade-offs made, and architectural insights gained"
    )
    technologies = models.ManyToManyField(
        ProjectTechnology,
        related_name='projects',
        blank=True
    )
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Primary project mockup or architecture diagram"
    )
    github_url = models.URLField(
        blank=True,
        help_text="Link to public GitHub repository (leave empty if proprietary or in-progress)"
    )
    live_url = models.URLField(
        blank=True,
        help_text="Link to live deployment or interactive demonstration"
    )
    featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Pin to the Featured Projects showcase on the homepage"
    )
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Uncheck to hide project from public view"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )
    date_created = models.DateField(
        auto_now_add=True,
        help_text="Date when project record was created"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-date_created']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
