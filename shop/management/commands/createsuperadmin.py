
import getpass

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser if one does not already exist'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Superuser '{username}' already exists. Skipped."
                )
            )
            return

        password = getpass.getpass('Enter superuser password: ')
        confirm = getpass.getpass('Confirm password: ')

        if not password:
            self.stderr.write(self.style.ERROR('Password cannot be empty.'))
            return

        if password != confirm:
            self.stderr.write(self.style.ERROR('Passwords do not match.'))
            return

        User.objects.create_superuser(
            username=username,
            email='',
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser '{username}' created successfully!"
            )
        )
