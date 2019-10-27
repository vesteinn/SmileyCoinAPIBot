from django.core.management.base import BaseCommand
import tqdm
from block.models import Block


class Command(BaseCommand):
    help = 'Populates database by connecting to smileycoin-daemon'

    def add_arguments(self, parser):
        parser.add_argument('from', type=int)
        parser.add_argument('to', type=int)

    def handle(self, *args, **options):

        for i in tqdm.tqdm(
                range(options.get('from', 0), options['to'])
        ):
            Block.new(block_id=i)
