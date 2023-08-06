import subprocess
from tempfile import mkdtemp

import click
import mongoengine
from click import echo

from .utils import temp_directory
from .models import Migration, MigrationHistoryStorage
from .query_sets import querysets


def establish_datastore_connection(environment):
    mongo_db_name = environment['db_name']

    args = {}
    args['host'] = environment['host']
    args['port'] = environment['port']
    if 'username' in environment:
        args['username'] = environment['username']
    if 'password' in environment:
        args['password'] = environment['password']

    # Using mongoengine connection logic for now
    # But consider dropping down to pymongo MongoClient
    # directly in the future
    return mongoengine.connect(mongo_db_name, **args)


class MongoMigrationHistory(MigrationHistoryStorage, mongoengine.Document):
    """
    Mongo Table to keep track of the status of migrations
    """
    key = mongoengine.StringField()
    state = mongoengine.StringField(default=Migration.STATE_NEW)
    processed_at = mongoengine.DateTimeField()

    @classmethod
    def find_or_create_by_key(cls, migration_key):
        return cls.objects.get_or_create(key=migration_key)[0]

    @classmethod
    def find_by_key(cls, migration_key):
        results = cls.objects(key=migration_key)
        if len(results) == 1:
            return results[0]
        else:
            return None

    @classmethod
    def all(cls):
        return cls.objects()


class MongoBackedMigration(Migration):

    def update_status(self, state):
        migration_meta = MongoMigrationHistory.find_or_create_by_key(self.migration_key)
        migration_meta.update(set__state=state)

    @property
    def status(self):
        migration_meta = MongoMigrationHistory.find_or_create_by_key(self.migration_key)
        return migration_meta.state


def dump_db(from_env, **kwargs):
    """accepts temp_dir and QuerySet as keyword options"""

    if 'temp_dir' in kwargs:
        temp_dir = kwargs['temp_dir']
    else:
        temp_dir = mkdtemp()

    if 'QuerySet' in kwargs:
        QuerySet = kwargs['QuerySet']

    echo("env: {}".format(from_env))

    options = {
        '-h': "{}:{}".format(from_env['host'], str(from_env['port'])),
        '-d': from_env['db_name'],
        '-o': temp_dir
    }
    if 'username' in from_env:
        options['-u'] = from_env['username']
    if 'password' in from_env:
        options['-p'] = from_env['password']

    if QuerySet:

        connection = establish_datastore_connection(from_env)
        database = connection[from_env['db_name']]

        query_set = QuerySet(database, options)

        query_set.execute()

    else:

        execution_array = ['mongodump']
        for option in options:
            execution_array.extend([option, options[option]])
        echo("Executing: {}".format(execution_array))
        subprocess.call(execution_array)

    # mongorestore -h localhost --drop -d spotlight db/backups/spotlight-staging-1/
    dump_path = "{}/{}".format(temp_dir, from_env['db_name'])
    return dump_path


def copy_db(from_env, to_env, query_set=None):
    with temp_directory() as temp_dir:
        # "mongodump -h dharma.mongohq.com:10067 -d spotlight-staging-1 -u spotlight -p V4Mld1ws4C5To0N -o db/backups/"
        dump_path = dump_db(from_env, temp_dir=temp_dir, QuerySet=query_set)
        restore(dump_path, to_env)


def restore(dump_path, to_env):
    # mongorestore -h localhost --drop -d spotlight db/backups/spotlight-staging-1/

    drop(to_env)

    options = {
        '-h': "{}:{}".format(to_env['host'], str(to_env['port'])),
        '-d': to_env['db_name'],
    }

    if 'username' in to_env:
        options['-u'] = to_env['username']

    if 'password' in to_env:
        options['-p'] = to_env['password']

    execution_array = ['mongorestore', '--drop']
    for option in options:
        execution_array.extend([option, options[option]])

    execution_array.append(dump_path)

    echo("Executing: {}".format(execution_array))
    subprocess.call(execution_array)


def drop(environ):

    options = {
        '--host': environ['host'],
        '--port': str(environ['port']),
        '--eval': '"db.dropDatabase()"'
    }

    execution_array = ['mongo', environ['db_name']]
    for option in options:
        execution_array.extend([option, options[option]])

    echo()
    echo("You are about to execute the following database drop")
    echo("    {}".format(' '.join(execution_array)))
    echo()
    click.confirm('ARE YOU SURE??', abort=True)

    subprocess.call(' '.join(execution_array), shell=True)
