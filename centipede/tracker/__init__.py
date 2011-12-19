import sys


def load_tracker(tracker_name):
    module, class_name = tracker_name.rsplit('.', 1)
    __import__(module)
    return getattr(sys.modules[module], class_name)()


class TrackerInterface(object):

    def get_ticket(self, ticket_id):
        raise NotImplementedError()

    def list_root(self):
        raise NotImplementedError()

    def list_children(self, ticket_id):
        raise NotImplementedError()
