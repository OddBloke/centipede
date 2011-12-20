import json

from django.test import Client
from mock import Mock, patch
from nose.tools import assert_equal, assert_true


def _get_ticket(prefix):
    return {
        'title': '{0} Title'.format(prefix),
        'description': '{0} Description'.format(prefix),
        'owner': '{0} Owner'.format(prefix),
        'state': '{0} State'.format(prefix),
        'identifier': '{0} Identifier'.format(prefix),
    }


class Get(object):

    def __init__(self):
        ticket_mock = Mock()
        ticket_mock.content = json.dumps(_get_ticket('Test'))
        child_mock = Mock()
        child_mock.content = json.dumps([_get_ticket('Child'),
                                         _get_ticket('Child2')])
        self.mocks = [ticket_mock, child_mock]

    def side_effect(self, *args):
        return self.mocks.pop(0)


@patch('centipede_ui.tickets.views.settings.CENTIPEDE_URL', 'http://centipede')
@patch('centipede_ui.centipedelib.requests.get')
def test_view_ticket(get):
    get.side_effect = Get().side_effect
    c = Client()
    response = c.get('/tickets/view/US123/')
    assert_equal(200, response.status_code)
    for string in ['Test Title', 'Test Description', 'Test Owner',
                   'Test State', 'Test Identifier']:
        assert_true(string in response.content,
                        '"{0}" not on page'.format(string))
    for prefix in ['Child', 'Child2']:
        for string in ['{0} Title', '{0} Owner', '{0} State',
                       '{0} Identifier']:
            expected = string.format(prefix)
            assert_true(expected in response.content,
                            '"{0}" not on page'.format(expected))
