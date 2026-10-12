from datetime import date, timedelta

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from studentportal import settings
from .forms import EventForm
from .models import Event, EventCertificate, EventRegistration, EventRequest
from .views import ensure_demo_data


class EventRequestTests(TestCase):
    def test_holo_lab_requires_login(self):
        response = self.client.get(reverse('holo_lab'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('holo_lab')}")

    def test_dashboard_links_to_holo_lab_and_lab_renders(self):
        user = User.objects.create_user(username='labuser', password='StrongPass123!')
        self.client.force_login(user)

        dashboard_response = self.client.get(reverse('dashboard'))
        lab_response = self.client.get(reverse('holo_lab'))

        self.assertContains(dashboard_response, reverse('holo_lab'))
        self.assertEqual(lab_response.status_code, 200)
        self.assertContains(lab_response, 'id="root"')
        self.assertContains(lab_response, '/static/holocloth/index-7o2sso0D.js')

    def test_holocloth_assets_require_login_and_serve_local_images(self):
        asset_url = reverse('holocloth_cloth_image')
        response = self.client.get(asset_url)
        self.assertRedirects(response, f"{reverse('login')}?next={asset_url}")

        user = User.objects.create_user(username='assetuser', password='StrongPass123!')
        self.client.force_login(user)
        response = self.client.get(asset_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/jpeg')
        self.assertGreater(int(response['Content-Length']), 1000)

    def test_database_falls_back_to_sqlite_when_mysql_is_unavailable(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

    def test_event_request_requires_user_and_title(self):
        user = User.objects.create_user(username='student1', password='StrongPass123!')
        request_obj = EventRequest.objects.create(
            user=user,
            title='AI Startup Expo',
            category='Technology',
            description='Need more tech events on campus.',
            preferred_date='2026-12-01',
        )

        self.assertEqual(request_obj.user.username, 'student1')
        self.assertEqual(request_obj.status, 'pending')

    def test_demo_data_is_not_seeded(self):
        ensure_demo_data()
        self.assertEqual(Event.objects.count(), 0)

    def test_event_form_rejects_past_dates(self):
        form = EventForm(data={
            'title': 'Past Event',
            'description': 'This event should fail validation.',
            'category': 'Technology',
            'location': 'Room A',
            'event_date': (date.today() - timedelta(days=1)).isoformat(),
            'start_time': '09:00:00',
            'end_time': '10:00:00',
            'capacity': 20,
            'is_published': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('event_date', form.errors)

    def test_event_supports_cover_image_field(self):
        self.assertTrue('cover_image' in [field.name for field in Event._meta.get_fields()])

    def test_event_certificate_model_supports_user_event_link(self):
        self.assertTrue('event' in [field.name for field in EventCertificate._meta.get_fields()])
        self.assertTrue('user' in [field.name for field in EventCertificate._meta.get_fields()])
        self.assertTrue('certificate_file' in [field.name for field in EventCertificate._meta.get_fields()])

    def test_event_analytics_requires_event_creator(self):
        organizer = User.objects.create_user(username='organizer1', password='StrongPass123!')
        other_organizer = User.objects.create_user(username='organizer2', password='StrongPass123!')
        event = Event.objects.create(
            organizer=organizer,
            title='Tech Meetup',
            description='A tech meetup',
            category='Technology',
            location='Room A',
            event_date=date.today() + timedelta(days=10),
            start_time='09:00:00',
            end_time='10:00:00',
            capacity=20,
            is_published=True,
        )

        self.client.force_login(other_organizer)
        response = self.client.get(reverse('event_analytics', args=[event.id]))

        self.assertEqual(response.status_code, 404)

    def test_event_analytics_page_renders_for_event_creator(self):
        organizer = User.objects.create_user(username='organizer3', password='StrongPass123!')
        event = Event.objects.create(
            organizer=organizer,
            title='Campus Startup Expo',
            description='A startup expo',
            category='Business',
            location='Auditorium',
            event_date=date.today() + timedelta(days=15),
            start_time='10:00:00',
            end_time='12:00:00',
            capacity=50,
            is_published=True,
        )
        user = User.objects.create_user(username='student1', password='StrongPass123!')
        EventRegistration.objects.create(user=user, event=event, status='selected')

        self.client.force_login(organizer)
        response = self.client.get(reverse('event_analytics', args=[event.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analytics Overview')
        self.assertContains(response, 'Campus Startup Expo')
        self.assertTrue(response.context['has_registration_data'])

    def test_event_analytics_handles_empty_registration_data(self):
        organizer = User.objects.create_user(username='organizer4', password='StrongPass123!')
        event = Event.objects.create(
            organizer=organizer,
            title='Empty Trend Event',
            description='An event without registrations yet',
            category='Technology',
            location='Lab 2',
            event_date=date.today() + timedelta(days=20),
            start_time='12:00:00',
            end_time='13:00:00',
            capacity=30,
            is_published=True,
        )

        self.client.force_login(organizer)
        response = self.client.get(reverse('event_analytics', args=[event.id]))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['has_registration_data'])
        self.assertContains(response, 'No registrations yet')
