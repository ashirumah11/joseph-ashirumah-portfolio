from django.test import TestCase, Client
from django.urls import reverse
from core.models import Profile, SkillCategory, Skill, Experience, SiteSettings


class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.load()
        self.profile.name = "Joseph Ashirumah"
        self.profile.headline = "Building reliable software for the web."
        self.profile.save()

        self.category = SkillCategory.objects.create(
            key="backend",
            display_name="Backend Engineering",
            icon="bi-server",
            order=1
        )
        self.skill = Skill.objects.create(
            category=self.category,
            name="Python",
            is_primary_stack=True,
            order=1
        )
        self.exp = Experience.objects.create(
            experience_type="work",
            title="Software Engineer",
            organization="Tech Co",
            start_date="2023",
            end_date="Present",
            is_current=True,
            description="Developing scalable web applications."
        )

    def test_homepage_status_code(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Joseph Ashirumah")
        self.assertContains(response, "Building reliable software for the web.")
        self.assertContains(response, "Python")

    def test_about_page_status_code(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Professional Background")
        self.assertContains(response, "Software Engineer")

    def test_robots_txt(self):
        response = self.client.get(reverse('core:robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn("User-agent: *", response.content.decode())
        self.assertIn("Sitemap:", response.content.decode())

    def test_sitemap_xml(self):
        response = self.client.get(reverse('core:sitemap_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn("<urlset", response.content.decode())

    def test_profile_singleton(self):
        p1 = Profile.load()
        p2 = Profile.load()
        self.assertEqual(p1.pk, 1)
        self.assertEqual(p2.pk, 1)
