from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = "Start the single-process in-memory demo server."
    def add_arguments(self, parser):
        parser.add_argument("--addrport", default="127.0.0.1:8000")
    def handle(self, *args, **options):
        # Migrate and serve in the same process; no-thread mode keeps the
        # in-memory SQLite connection shared across local requests.
        call_command("migrate", interactive=False, verbosity=0)
        call_command("seed_demo", verbosity=0)
        call_command("runserver", options["addrport"], "--nothreading", "--noreload")
