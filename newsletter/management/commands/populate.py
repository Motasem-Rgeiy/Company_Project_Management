from faker import Faker
from django.core.management.base import BaseCommand
from newsletter.models import Subscriber
from django.db import transaction, DatabaseError


fake = Faker()

#Run by: docker compose exec djangoserver python manage.py populate
class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):

        # create subscribers: email, is_active, created_at, updated_at
            subscribers = []
            for _ in range(1000):
                subscribers.append(
                    Subscriber(email=fake.unique.email(), is_active=True)
                )
            try:

            # create subscribers
                with transaction.atomic():
                    Subscriber.objects.bulk_create(subscribers)

                print('1000 subscribers are successfully created.')

            except DatabaseError as e:
                 print(f'Database Error: {e}')
            except Exception as e:
                print(f'Error: {e}')


