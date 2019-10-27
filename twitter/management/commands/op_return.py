from django.core.management.base import BaseCommand
from twitter.models import OpReturn


class Command(BaseCommand):
    help = 'Looks for interesting op return messages'

    def handle(self, *args, **options):
        OpReturn.update()