from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Project, ProjectTechnology


def project_list(request):
    """
    Archive of software engineering projects with technology filtering
    and search capabilities.
    """
    tech_filter = request.GET.get('tech', '').strip()
    search_query = request.GET.get('q', '').strip()

    projects = Project.objects.filter(is_published=True).prefetch_related('technologies')

    selected_tech = None
    if tech_filter:
        selected_tech = ProjectTechnology.objects.filter(slug=tech_filter).first()
        if selected_tech:
            projects = projects.filter(technologies=selected_tech)

    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(problem_statement__icontains=search_query) |
            Q(solution_statement__icontains=search_query) |
            Q(architecture_description__icontains=search_query)
        )

    all_technologies = ProjectTechnology.objects.filter(
        projects__is_published=True
    ).distinct().order_by('name')

    context = {
        'projects': projects,
        'all_technologies': all_technologies,
        'selected_tech': selected_tech,
        'search_query': search_query,
        'total_projects_count': projects.count(),
    }
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    """
    Detailed engineering case study page breaking down problem statement,
    architectural decisions, database modeling, challenges, and live demos.
    """
    project = get_object_or_404(
        Project.objects.prefetch_related('technologies'),
        slug=slug,
        is_published=True
    )

    # Key features split if formatted as lines/bullets
    features_list = [
        feat.strip()
        for feat in project.key_features.split('\n')
        if feat.strip()
    ]

    # Related projects
    related_projects = (
        Project.objects.filter(is_published=True)
        .exclude(pk=project.pk)
        .prefetch_related('technologies')[:3]
    )

    context = {
        'project': project,
        'features_list': features_list,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)
