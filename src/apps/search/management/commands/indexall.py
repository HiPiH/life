from django.core.management.base import NoArgsCommand, CommandError
from apps.search import finder

finder.autodiscover()

class Command(NoArgsCommand):
    
    def handle_noargs(self, requires_model_validation=False, **options):
        finder.search_manager.index_all()