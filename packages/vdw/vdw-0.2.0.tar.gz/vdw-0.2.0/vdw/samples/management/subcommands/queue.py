import os
import redis
import glob
import logging
from django_rq import get_worker
from rq import Worker
from redis.exceptions import ConnectionError
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS
from vdw.samples.pipeline.handlers import load_samples

SAMPLE_DIRS = getattr(settings, 'VARIFY_SAMPLE_DIRS', ())

log = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
                    default=DEFAULT_DB_ALIAS,
                    help='Specifies the target database loading results.'),
        make_option('--max', action='store', dest='max', default=None,
                    type='int',
                    help='Specifies the maximum number of samples to queue.'),
        make_option('--startworkers', action='store_true', dest='startworkers',
                    default=False,
                    help='Include --startworkers flag to automatically start '
                         'the variant and default workers if they are not '
                         'already running. The workers will automatically '
                         'burst after the job is finished but will block the '
                         'terminal until the queues are emptied and all jobs '
                         'are finished.'),
    )

    def _queue(self, dirs, max_count, database, verbosity):
        count = 0
        skipped = 0
        scanned = 0

        # Walk the directory tree of each sample dirs to find all sample
        # directories with a valid MANIFEST file
        for source in dirs:
            log.debug('Scanning source directory: {0}'.format(source))

            for root, dirs, files in os.walk(source):
                if max_count and count == max_count:
                    return count, scanned

                if 'MANIFEST' not in files:
                    continue

                manifest_path = os.path.join(root, 'MANIFEST')

                try:
                    load_dict = load_samples(manifest_path, database)
                except Exception:
                    log.exception('error processing manifest {0}'
                                  .format(manifest_path))
                    continue

                if not load_dict:
                    continue

                count += load_dict['created']
                skipped += load_dict['skipped']
                if load_dict['created'] > 0:
                    if verbosity > 1:
                        log.debug('Queued sample: "{0}"'.format(root))
                elif verbosity > 2:
                    if load_dict['created'] == 0:
                        log.debug('Sample already loaded: "{0}"'.format(root))
                    else:
                        log.debug('Sample skipped: "{0}"'.format(root))

                scanned += 1

                # Print along the way since this is the only output for this
                # verbosity level
                if verbosity == 1:
                    log.debug(
                        "Queued {0} samples (max {1}) {2} skipped of {3} "
                        "scanned".format(count, max_count, skipped, scanned))

        return count, scanned

    def startWorkers(self):
        # Find the number of current workers
        queues = getattr(settings, 'RQ_QUEUES', {})
        default = queues['default'] if 'default' in queues else None
        variants = queues['variants'] if 'variants' in queues else None

        if not (queues and default and variants):
            log.warning('RQ_QUEUES settings could not be found')
            return

        # Create connections to redis to identify the workers
        def_connection = redis.Redis(host=default['HOST'],
                                     port=default['PORT'],
                                     db=default['DB'])
        var_connection = redis.Redis(host=variants['HOST'],
                                     port=variants['PORT'],
                                     db=variants['DB'])

        # Get all the workers connected with our redis server
        try:
            all_workers = Worker.all(def_connection) + \
                Worker.all(var_connection)
        except ConnectionError:
            log.warning('Could not connect to redis server to create workers. '
                        'Please make sure Redis server is running')
            return

        found_default = False
        found_variant = False

        # Loop through all the workers (even duplicates)
        for worker in all_workers:
            found_default = found_default or 'default' in worker.queue_names()
            found_variant = found_variant or 'variants' in worker.queue_names()

        # Start the required worker
        if not found_variant:
            log.debug('Did not find variants worker. Starting ... ')
            get_worker('variants').work(burst=True)

        if not found_default:
            log.debug('Did not find default worker. Starting ... ')
            get_worker('default').work(burst=True)

    def handle(self, *dirs, **options):
        database = options.get('database')
        max_count = options.get('max')
        verbosity = int(options.get('verbosity'))
        workers = options.get('startworkers')

        if not dirs:
            dirs = []
            for _dir in SAMPLE_DIRS:
                dirs.extend(glob.glob(_dir))

        count, scanned = self._queue(dirs, max_count, database, verbosity)

        if verbosity > 1:
            log.debug('Queued {0} samples (max {1}) of {2} scanned'.format(
                count, max_count, scanned))

        else:
            # Add a newline since the verbosity=1 output is written in-place
            # with a carriage return
            print ''

        # Start workers when appropriate
        if workers:
            self.startWorkers()
