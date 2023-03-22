import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command



class Command(BaseCommand):

    def handle(self, *args, **options):
        
        for replica in ['default'] + settings.REPLICATED_DATABASE_SLAVES:
            
            self.stdout.write(self.style.NOTICE('Applying Migrations for %s' % replica))
            call_command('migrate', '--database', replica)