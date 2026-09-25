from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a default superuser for local development"

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Superuser username')
        parser.add_argument('--email', default='admin@example.com', help='Superuser email')
        parser.add_argument('--password', default='admin12345', help='Superuser password')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists. Updating password..."))
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"[OK] Password updated for superuser '{username}'"))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"[OK] Superuser '{username}' created successfully!"))
