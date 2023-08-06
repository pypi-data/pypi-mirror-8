# coding=utf-8
from pyramid_debugtoolbar.panels import DebugPanel

from pyramid_debugtoolbar_mongo import operation_tracker


try:
    import pymongo

    has_mongo = True
except ImportError:
    has_mongo = False

__author__ = 'gillesdevaux'


class MongoDebugPanel(DebugPanel):
    """Panel that shows information about MongoDB operations.
    """
    name = 'MongoDB'
    has_content = has_mongo
    nav_title = 'MongoDB'
    title = 'MongoDB Operations'
    template = 'pyramid_debugtoolbar_mongo.panels:templates/mongo.dbtmako'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        operation_tracker.install_tracker()
        operation_tracker.reset()

    @property
    def nav_subtitle(self):
        num_operations = len(operation_tracker.queries)
        attrs = ['queries', 'inserts', 'updates', 'removes']
        total_time = sum(sum(o['time'] for o in getattr(operation_tracker, a)) for a in attrs)
        return '{0} operations in {1:.2f}ms'.format(num_operations, total_time)

    def render_vars(self, request):
        return {
            'queries': operation_tracker.queries,
            'inserts': operation_tracker.inserts,
            'updates': operation_tracker.updates,
            'removes': operation_tracker.removes
        }
