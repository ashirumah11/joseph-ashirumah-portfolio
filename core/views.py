from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse
from .models import (
    Profile,
    SkillCategory,
    Skill,
    Experience,
    ValuePillar,
    SiteSettings,
)
from projects.models import Project
from contact.forms import ContactForm


def home_view(request):
    """
    Primary landing page showcasing:
    - Hero with developer terminal and interactive CTA buttons
    - Short bio & core specialization (Python + Django + SQL)
    - Categorized skills
    - Featured software engineering projects
    - Engineering value pillars (Why Work With Me)
    - Professional experience, education, & certifications timeline
    - Interactive Contact form
    """
    # Fetch skill categories with their active skills
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    primary_skills = Skill.objects.filter(is_primary_stack=True).select_related('category')

    # Fetch projects
    featured_projects = (
        Project.objects.filter(is_published=True, featured=True)
        .prefetch_related('technologies')
        .order_by('display_order', '-date_created')[:6]
    )
    
    other_projects = (
        Project.objects.filter(is_published=True, featured=False)
        .prefetch_related('technologies')
        .order_by('display_order', '-date_created')[:4]
    )

    # Experience & Journey breakdown
    work_experiences = Experience.objects.filter(
        experience_type__in=['work', 'milestone']
    ).order_by('order', '-id')

    education_list = Experience.objects.filter(
        experience_type='education'
    ).order_by('order', '-id')

    certifications_list = Experience.objects.filter(
        experience_type='certification'
    ).order_by('order', '-id')

    # Value pillars
    value_pillars = ValuePillar.objects.all().order_by('order')

    # Contact form
    contact_form = ContactForm()

    context = {
        'skill_categories': skill_categories,
        'primary_skills': primary_skills,
        'featured_projects': featured_projects,
        'other_projects': other_projects,
        'work_experiences': work_experiences,
        'education_list': education_list,
        'certifications_list': certifications_list,
        'value_pillars': value_pillars,
        'contact_form': contact_form,
    }
    return render(request, 'home.html', context)


def about_view(request):
    """
    Dedicated About Me page detailing engineering background,
    technical architecture approach, education, and career vision.
    """
    work_experiences = Experience.objects.filter(
        experience_type__in=['work', 'milestone']
    ).order_by('order', '-id')

    education_list = Experience.objects.filter(
        experience_type='education'
    ).order_by('order', '-id')

    certifications_list = Experience.objects.filter(
        experience_type='certification'
    ).order_by('order', '-id')

    value_pillars = ValuePillar.objects.all().order_by('order')
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()

    context = {
        'work_experiences': work_experiences,
        'education_list': education_list,
        'certifications_list': certifications_list,
        'value_pillars': value_pillars,
        'skill_categories': skill_categories,
    }
    return render(request, 'about.html', context)


@require_GET
def robots_txt(request):
    """Serve robots.txt file allowing web search indexing."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri(reverse('core:sitemap_xml'))}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def sitemap_xml(request):
    """Generate dynamic XML sitemap for SEO."""
    base_url = request.build_absolute_uri('/').rstrip('/')
    published_projects = Project.objects.filter(is_published=True).order_by('-updated_at')

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        f'    <loc>{base_url}{reverse("core:home")}</loc>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}{reverse("core:about")}</loc>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.8</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}{reverse("projects:project_list")}</loc>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.9</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{base_url}{reverse("contact:contact_page")}</loc>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.7</priority>',
        '  </url>',
    ]

    for project in published_projects:
        xml_lines.extend([
            '  <url>',
            f'    <loc>{base_url}{project.get_absolute_url()}</loc>',
            f'    <lastmod>{project.updated_at.strftime("%Y-%m-%d")}</lastmod>',
            '    <changefreq>monthly</changefreq>',
            '    <priority>0.8</priority>',
            '  </url>',
        ])

    xml_lines.append('</urlset>')
    return HttpResponse("\n".join(xml_lines), content_type="application/xml")


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
