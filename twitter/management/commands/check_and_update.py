from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Max

from twitter.models import Push

from block.utils import get_highest_block


class Command(BaseCommand):
    help = 'Updates the database, scans op_returns and posts to twitter'

    def handle(self, *args, **options):

        last_block = Push.objects.all().aggregate(Max('block_height'))['block_height__max']
        if last_block is None:
            last_block = 0

        highest_block = get_highest_block()

        call_command('scrape', last_block + 1, highest_block + 1)
        call_command('op_return')
        call_command('update_twitter')

        Push.objects.create(block_height=highest_block)
