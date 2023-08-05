"""
Cache engines are used as an intermediate store for computed report data.
Since pulling and processing the data for a report can be computationally
intensive, this cached storage allows us to sort and page through the
resulting report very quickly and easily.

Currently, the easiest to get up and running is :doc:`/caches/local_cache`, as
it has no dependencies outside of Python and simply caches to the local
filesystem. However, it cannot handle concurrent connections and is generally
a poor choice outside of the development environment. At the moment, the
preferred choice for deployment is :doc:`/caches/redis_cache`.
"""
from functools import wraps


class InstanceLockError(Exception):
    """Cannot secure a lock on writing the instance to cache."""

class InstanceExistsError(Exception):
    """Cannot record the instance because it already exists in cache."""

class InstanceIncompleteError(Exception):
    """The instance has not yet finished being created in cache."""

class Cache(object):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create_instance(self, report_id, instance_id, rows, footer, expire):
        raise NotImplementedError

    def kill_instance_cache(self, report_id, instance_id):
        raise NotImplementedError

    def kill_report_cache(self, report_id):
        raise NotImplementedError

    def is_instance_started(self, report_id, instance_id):
        raise NotImplementedError

    def is_instance_finished(self, report_id, instance_id):
        raise NotImplementedError

    def instance_row_count(self, report_id, instance_id):
        raise NotImplementedError

    def instance_timestamp(self, report_id, instance_id):
        raise NotImplementedError

    def instance_rows(self, report_id, instance_id, selected=None, sort=None, limit=None, offset=None, alpha=False):
        raise NotImplementedError

    def instance_footer(self, report_id, instance_id):
        raise NotImplementedError

def cache_connection(func):
    """
    Function decorator to run the function within the context of the cache.
    
    Will look for the cache first as a kwarg to the function named `cache`,
    then as the attribute `self.cache`. If neither is found, it will be an
    error.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        if 'cache' in kwargs:
            cache = kwargs['cache']
        elif args and hasattr(args[0], 'cache'):
            cache = args[0].cache
        else:
            raise ValueError('Could not find cache as keyword argument or '
                'on self to create the cache context.')
        with cache:
            return func(*args, **kwargs)
    return wrapped
