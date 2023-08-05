#!/usr/bin/env python

from __future__ import absolute_import

import argparse
import collections
import os
import sys
import yaml


EXTRA_CHECK_MAKERS = []
STATSD_CHECK = {
    'send': 'conncheck.test:1|c',
    'expect': '',
}


class SettingsDict(dict):
    """Wrapper for Django settings object that allows access as a dict"""

    def __init__(self, settings):
        self.settings = settings

    def __getitem__(self, name):
        return getattr(self.settings, name, None)

    def get(self, name, default):
        return getattr(self.settings, name, default)


def get_settings(settings_module):
    if settings_module:
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    from django.conf import settings as django_settings
    return SettingsDict(django_settings)


def make_postgres_checks(settings, options):
    checks = []
    for name, db in settings.get('DATABASES', {}).items():
        if db.get('ENGINE') == 'django.db.backends.postgresql_psycopg2':
            checks.append({
                'type': 'postgres',
                'database': db.get('NAME', options.db_name),
                'host': db['HOST'],
                'port': int(db['PORT']),
                'username': db['USER'],
                'password': db['PASSWORD'],
            })
    return checks


def make_oops_checks(settings, options):
    checks = []
    oopses = settings.get('OOPSES', {})
    publishers = oopses.get('publishers', [])
    for publisher in publishers:
        if publisher['type'] == 'amqp':
            checks.append({
                'type': 'amqp',
                'vhost': publisher['vhost'],
                'host': publisher['host'],
                'port': publisher.get('port', 5672),
                'username': publisher['user'],
                'password': publisher['password'],
            })
    return checks


def make_celery_checks(settings, options):
    # XXX: this is the old style of celery config
    # TODO add support for new style config
    checks = []
    host = settings['BROKER_HOST']
    backend = settings['BROKER_BACKEND']
    if ((not backend and host) or backend in ('amqp', 'redis')):
        check = {
            'type': backend,
            'host': host,
            'port': int(settings['BROKER_PORT']),
            'username': settings['BROKER_USER'],
            'password': settings['BROKER_PASSWORD'],
        }
        if settings['BROKER_VHOST']:
            check['vhost'] = settings['BROKER_VHOST']
        checks.append(check)
    return checks


def make_memcache_checks(settings, options):
    checks = []
    caches = settings.get('CACHES', {})

    for cache in caches.values():
        backend = cache['BACKEND']
        if (not backend or backend ==
                'django.core.cache.backends.memcached.MemcachedCache'):

            locations = cache['LOCATION']
            if not isinstance(locations, collections.Iterable):
                locations = [locations]

            for location in locations:
                host, port = location.split(':')
                checks.append({
                    'type': 'memcached',
                    'host': host,
                    'port': int(port),
                })

    return checks


def make_statsd_checks(settings, options):
    # For now we just want to make sure we can reach statsd via UDP
    checks = []
    if settings['STATSD_HOST']:
        checks.append({
            'type': 'udp',
            'host': settings['STATSD_HOST'],
            'port': int(settings.get('STATSD_PORT', 8125)),
            'send': statsd_send,
            'expect': statsd_expect,
        })
    return checks


def gather_checks(options):
    settings = get_settings(options.settings_module)
    checks = []
    checks.extend(make_postgres_checks(settings, options))
    checks.extend(make_oops_checks(settings, options))
    checks.extend(make_celery_checks(settings, options))
    checks.extend(make_memcache_checks(settings, options))
    checks.extend(make_statsd_checks(settings, options))

    for maker in EXTRA_CHECK_MAKERS:
        checks.extend(maker(settings, options))

    return checks


def main(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file')
    parser.add_argument('-m', '--settings-module',
                        dest="settings_module",
                        action="store")
    parser.add_argument('-d', '--database-name',
                        dest="db_name",
                        action="store")
    parser.add_argument('--statsd_send',
                        dest="statsd_send",
                        action="store")
    parser.add_argument('--statsd_expect',
                        dest="statsd_expect",
                        action="store")
    opts = parser.parse_args(args)

    if opts.statsd_send:
        STATSD_CHECK['send'] = opts.statsd_send

    if opts.statsd_expect:
        STATSD_CHECK['expect'] = opts.statsd_expect

    checks = gather_checks(opts)

    with open(opts.output_file, 'w') as f:
        yaml.dump(checks, f, default_flow_style=False)

    return 0


def run():
    exit(main(*sys.argv[1:]))


if __name__ == '__main__':
    run()
