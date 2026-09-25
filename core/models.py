from django.db import models
from django.core.exceptions import ValidationError


class SingletonModel(models.Model):
    """Abstract singleton model ensuring only one instance exists."""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Profile(SingletonModel):
    name = models.CharField(max_length=150, default="Joseph Ashirumah")
    professional_title = models.CharField(max_length=200, default="Full-Stack Software Engineer")
    eyebrow_text = models.CharField(
        max_length=150,
        default="FULL-STACK SOFTWARE ENGINEER",
        help_text="Small eyebrow tag above the main hero headline"
    )
    headline = models.CharField(
        max_length=255,
        default="I build software that solves real problems."
    )
    subheadline = models.TextField(
        default="I'm a Full-Stack Software Engineer specializing in Python, Django, SQL and modern frontend development. I enjoy turning ideas into reliable, maintainable web applications."
    )
    short_bio = models.TextField(
        default="Full-stack engineer passionate about building practical, dependable software with Python, Django, and modern web architectures."
    )
    about_text = models.TextField(
        default="""I’m a Full-Stack Software Engineer focused on building practical, maintainable and scalable web applications. My core specialization is Python and Django on the backend, SQL and relational databases for data management, and modern frontend technologies for building responsive user experiences.

I approach software engineering with a product-oriented mindset—prioritizing robust data schemas, clean API interfaces, intuitive UX, and clean code that teams can confidently maintain and extend. Whether architecting backend business logic or polishing frontend interactions, I build solutions engineered for performance, security, and long-term reliability."""
    )
    profile_photo = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        help_text="Professional headshot or profile photo"
    )
    cv_file = models.FileField(
        upload_to='cv/',
        blank=True,
        null=True,
        help_text="Upload your resume / CV document (PDF recommended)"
    )
    email = models.EmailField(default="joseph.ashirumah@example.com")
    phone = models.CharField(max_length=60, blank=True, default="+1 (555) 000-0000 [EDIT THIS]")
    location = models.CharField(max_length=150, default="Available for Remote & Relocation [EDIT THIS]")
    status_badge = models.CharField(
        max_length=120,
        default="Open to Software Engineering Opportunities",
        help_text="Visible badge indicating your current availability"
    )
    status_active = models.BooleanField(
        default=True,
        help_text="Toggle visibility of the availability status indicator"
    )
    github_url = models.URLField(blank=True, default="https://github.com/ashirumah11")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/in/josephashirumah [EDIT THIS]")
    twitter_url = models.URLField(blank=True, default="")
    hero_code_snippet = models.TextField(
        blank=True,
        default="""# developer_profile.py

class SoftwareEngineer:
    def __init__(self):
        self.name = "Joseph Ashirumah"
        self.role = "Full-Stack Software Engineer"
        self.stack = ["Python", "Django", "PostgreSQL", "JavaScript"]
        self.focus = "Reliable, maintainable systems"

    def status(self):
        return "Building & open to opportunities" """,
        help_text="Python code preview rendered in the interactive hero terminal card"
    )

    class Meta:
        verbose_name = "Profile & Bio"
        verbose_name_plural = "Profile & Bio"

    def __str__(self):
        return f"{self.name} - {self.professional_title}"


class SkillCategory(models.Model):
    CATEGORY_KEYS = [
        ('backend', 'Backend Engineering'),
        ('frontend', 'Frontend Development'),
        ('database', 'Database & Data Systems'),
        ('tools', 'Tools & DevOps'),
    ]

    key = models.CharField(max_length=40, choices=CATEGORY_KEYS, unique=True)
    display_name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=80,
        default="bi-cpu",
        help_text="Bootstrap icon class (e.g. bi-server, bi-code-slash, bi-database, bi-gear)"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'display_name']
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.display_name


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100)
    icon_class = models.CharField(
        max_length=80,
        blank=True,
        help_text="Bootstrap or Devicon class, e.g. bi-filetype-py, bi-database, bi-git"
    )
    is_primary_stack = models.BooleanField(
        default=False,
        help_text="Mark as part of the core highlighted stack (e.g. Python, Django, SQL)"
    )
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short highlight, e.g. 'ORM modeling, authentication & scalable services'"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Skill / Technology"
        verbose_name_plural = "Skills & Technologies"

    def __str__(self):
        return f"{self.name} ({self.category.display_name})"


class Experience(models.Model):
    EXPERIENCE_TYPES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
        ('certification', 'Certification'),
        ('milestone', 'Milestone & Project Journey'),
    ]

    experience_type = models.CharField(
        max_length=30,
        choices=EXPERIENCE_TYPES,
        default='work'
    )
    title = models.CharField(
        max_length=180,
        help_text="Job title, degree, or certificate name"
    )
    organization = models.CharField(
        max_length=180,
        help_text="Company, University, or Issuing Authority"
    )
    location = models.CharField(max_length=120, blank=True)
    start_date = models.CharField(max_length=60, help_text="e.g. 2023 or Jan 2023")
    end_date = models.CharField(
        max_length=60,
        blank=True,
        help_text="e.g. Present or Dec 2024 (leave blank if current)"
    )
    is_current = models.BooleanField(default=False)
    description = models.TextField(
        help_text="Key responsibilities, architectural accomplishments, technologies used, or course summary"
    )
    credential_url = models.URLField(
        blank=True,
        help_text="Optional link to credential, company, or course verification"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Experience / Journey Entry"
        verbose_name_plural = "Experience & Journey Entries"

    def __str__(self):
        return f"[{self.get_experience_type_display()}] {self.title} @ {self.organization}"


class ValuePillar(models.Model):
    """
    'Why Work With Me' pillars highlighting engineering mindset:
    Full-Stack Thinking, Backend Focus, Database Driven, Product Mindset, Continuous Growth
    """
    title = models.CharField(max_length=120)
    icon = models.CharField(
        max_length=80,
        default="bi-check-circle",
        help_text="Bootstrap icon class (e.g. bi-layers, bi-server, bi-database-check, bi-lightbulb, bi-graph-up-arrow)"
    )
    short_summary = models.TextField(help_text="Concise description of the engineering value provided")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Why Work With Me Card"
        verbose_name_plural = "Why Work With Me Cards"

    def __str__(self):
        return self.title


class SocialLink(models.Model):
    PLATFORMS = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('x', 'X (Twitter)'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email (mailto)'),
        ('website', 'Portfolio / Blog'),
    ]

    platform = models.CharField(max_length=30, choices=PLATFORMS)
    label = models.CharField(max_length=60, blank=True, help_text="Display label, e.g. 'GitHub'")
    url = models.CharField(max_length=255, help_text="Destination URL or mailto: link")
    icon_class = models.CharField(
        max_length=60,
        default="bi-link-45deg",
        help_text="Bootstrap icon (e.g. bi-github, bi-linkedin, bi-twitter-x, bi-envelope)"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'platform']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return f"{self.get_platform_display()} ({self.url})"


class SiteSettings(SingletonModel):
    site_title = models.CharField(
        max_length=150,
        default="Joseph Ashirumah | Full-Stack Software Engineer"
    )
    meta_description = models.TextField(
        default="Portfolio of Joseph Ashirumah, Full-Stack Software Engineer specializing in Python, Django, SQL, and robust modern web architectures."
    )
    footer_text = models.CharField(
        max_length=255,
        default="Crafting scalable web applications with clean architecture and modern engineering standards."
    )
    contact_email = models.EmailField(default="joseph.ashirumah@example.com")
    enable_contact_form = models.BooleanField(default=True)
    enable_hire_cta = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_title
