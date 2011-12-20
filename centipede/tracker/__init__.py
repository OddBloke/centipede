import sys

from django.conf import settings


def load_tracker(tracker_name):
    module, class_name = tracker_name.rsplit('.', 1)
    __import__(module)
    return getattr(sys.modules[module], class_name)(settings)


class TrackerInterface(object):

    def __init__(self, settings=None):
        pass

    def get_ticket(self, ticket_id):
        raise NotImplementedError()

    def list_root(self):
        raise NotImplementedError()

    def list_children(self, ticket_id):
        raise NotImplementedError()
