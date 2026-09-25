from django.test import TestCase, Client
from django.urls import reverse
from projects.models import Project, ProjectTechnology


class ProjectsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tech_django = ProjectTechnology.objects.create(name="Django")
        self.tech_sql = ProjectTechnology.objects.create(name="SQL")

        self.project1 = Project.objects.create(
            title="Telemetry Dashboard",
            short_description="Distributed task telemetry system.",
            problem_statement="Monitoring worker starvation.",
            solution_statement="Real-time dashboard in Django.",
            architecture_description="Celery, Redis, and PostgreSQL.",
            key_features="Heartbeats and metrics.",
            challenges_and_learnings="Connection pooling solved.",
            featured=True,
            is_published=True,
            display_order=1
        )
        self.project1.technologies.add(self.tech_django, self.tech_sql)

        self.unpublished_project = Project.objects.create(
            title="Unpublished Internal Tool",
            short_description="Not ready for public.",
            problem_statement="Internal ops.",
            solution_statement="Internal script.",
            architecture_description="CLI.",
            key_features="Scripts.",
            challenges_and_learnings="None.",
            featured=False,
            is_published=False
        )

    def test_project_slug_auto_generation(self):
        self.assertEqual(self.project1.slug, "telemetry-dashboard")

    def test_project_list_view(self):
        response = self.client.get(reverse('projects:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Telemetry Dashboard")
        self.assertNotContains(response, "Unpublished Internal Tool")

    def test_project_filter_by_tech(self):
        response = self.client.get(reverse('projects:project_list') + '?tech=django')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Telemetry Dashboard")

    def test_project_search_query(self):
        response = self.client.get(reverse('projects:project_list') + '?q=telemetry')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Telemetry Dashboard")

    def test_project_detail_view(self):
        response = self.client.get(reverse('projects:project_detail', kwargs={'slug': self.project1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Telemetry Dashboard")
        self.assertContains(response, "Monitoring worker starvation.")
        self.assertContains(response, "Technical Architecture &amp; Data Layer Design")

    def test_project_detail_404_for_unpublished(self):
        response = self.client.get(reverse('projects:project_detail', kwargs={'slug': self.unpublished_project.slug}))
        self.assertEqual(response.status_code, 404)
