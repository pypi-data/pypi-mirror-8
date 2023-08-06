from __future__ import print_function

import os
from optparse import make_option

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField, ImageField, get_models

from database_files.models import File

class Command(BaseCommand):
    args = ''
    help = 'Deletes all files in the database that are not referenced by ' + \
        'any model fields.'
    option_list = BaseCommand.option_list + (
        make_option('--dryrun',
            action='store_true',
            dest='dryrun',
            default=False,
            help='If given, only displays the names of orphaned files ' + \
                'and does not delete them.'),
        )

    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        names = set()
        dryrun = options['dryrun']
        try:
            for model in get_models():
                print('Checking model %s...' % (model,))
                for field in model._meta.fields:
                    if not isinstance(field, (FileField, ImageField)):
                        continue
                    # Ignore records with null or empty string values.
                    q = {'%s__isnull'%field.name:False}
                    xq = {field.name:''}
                    subq = model.objects.filter(**q).exclude(**xq)
                    subq_total = subq.count()
                    subq_i = 0
                    for row in subq.iterator():
                        subq_i += 1
                        if subq_i == 1 or not subq_i % 100:
                            print('%i of %i' % (subq_i, subq_total))
                        file = getattr(row, field.name)
                        if file is None:
                            continue
                        if not file.name:
                            continue
                        names.add(file.name)
            # Find all database files with names not in our list.
            print('Finding orphaned files...')
            orphan_files = File.objects.exclude(name__in=names).only('name', 'size')
            total_bytes = 0
            orphan_total = orphan_files.count()
            orphan_i = 0
            print('Deleting %i orphaned files...' % (orphan_total,))
            for f in orphan_files.iterator():
                orphan_i += 1
                if orphan_i == 1 or not orphan_i % 100:
                    print('%i of %i' % (orphan_i, orphan_total))
                total_bytes += f.size
                if dryrun:
                    print('File %s is orphaned.' % (f.name,))
                else:
                    print('Deleting orphan file %s...' % (f.name,))
                    default_storage.delete(f.name)
            print('%i total bytes in orphan files.' % total_bytes)
        finally:
            settings.DEBUG = tmp_debug
