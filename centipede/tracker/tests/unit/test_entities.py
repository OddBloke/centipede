from nose.tools import assert_equal

from centipede.tracker.entities import Ticket


def test_ticket_as_dict():
    t = Ticket('identifier', 'description', 'title', 'owner', 'state')
    assert_equal({
        'identifier': 'identifier',
        'description': 'description',
        'title': 'title',
        'owner': 'owner',
        'state': 'state',
    }, t.as_dict())
