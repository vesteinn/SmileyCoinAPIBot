from django.core.management.base import BaseCommand

from twitter.client import TwitterClient
from twitter.models import OpReturn


class Command(BaseCommand):
    help = 'Looks for interesting op return messages'

    def handle(self, *args, **options):
        to_send = OpReturn.objects.filter(
            interesting=True,
            posted=False
        )

        tc = TwitterClient()
        tc.authenticate()

        for op in to_send:
            try:
                tc.api.update_status(op.format())
                op.posted = True
                op.save()
            except Exception as e:
                print("Something went wrong for {} - {}".format(op.id, op.format()))
                print(e)