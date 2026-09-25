from django.test import TestCase, Client
from django.urls import reverse
from contact.models import ContactMessage
from contact.forms import ContactForm


class ContactTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_page_loads(self):
        response = self.client.get(reverse('contact:contact_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Let's Discuss Software Engineering")

    def test_valid_contact_submission(self):
        payload = {
            'name': 'Alice Recruiter',
            'email': 'alice@techcompany.com',
            'subject': 'Senior Full-Stack Engineer Opportunity',
            'message': 'We reviewed your portfolio and would like to discuss our backend Python & Django role.',
            'confirm_website': '',  # Honeypot empty for valid users
        }
        response = self.client.post(reverse('contact:submit'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify message created in database
        msg = ContactMessage.objects.filter(email='alice@techcompany.com').first()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.name, 'Alice Recruiter')
        self.assertEqual(msg.subject, 'Senior Full-Stack Engineer Opportunity')
        self.assertFalse(msg.is_read)

    def test_honeypot_spam_rejection(self):
        payload = {
            'name': 'Spam Bot',
            'email': 'bot@spammer.com',
            'subject': 'Buy crypto',
            'message': 'Spam link advertising something bad.',
            'confirm_website': 'http://spam-site.com',  # Filled honeypot
        }
        response = self.client.post(reverse('contact:submit'), data=payload, follow=True)
        # Message should NOT be created
        self.assertEqual(ContactMessage.objects.filter(email='bot@spammer.com').count(), 0)

    def test_ajax_submission_response(self):
        payload = {
            'name': 'Bob Manager',
            'email': 'bob@startup.io',
            'subject': 'Django Consulting',
            'message': 'Need advice on scaling our database schema and optimizing queries.',
            'confirm_website': '',
        }
        response = self.client.post(
            reverse('contact:submit'),
            data=payload,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_ACCEPT='application/json',
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertIn("sent successfully", json_data['message'])

    def test_invalid_email_validation(self):
        payload = {
            'name': 'Test User',
            'email': 'invalid-email-address',
            'subject': 'Hi',
            'message': 'Too short',
            'confirm_website': '',
        }
        response = self.client.post(
            reverse('contact:submit'),
            data=payload,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_ACCEPT='application/json',
        )
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('email', json_data['errors'])
