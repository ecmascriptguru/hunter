from django.conf import settings
from django.core.management import BaseCommand
from ...tasks import validate_targets
from ...models import Target


class Command(BaseCommand):
    """
    Command to pull proxies from proxy providers and push them into database.
    """

    def handle(self, *args, **options):
        todos = Target.todos()
        if todos.exists():
            _, msg = validate_targets([todos.first().pk])
            self.stdout.write(msg, ending='')