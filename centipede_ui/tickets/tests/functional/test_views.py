import json

from django.test import Client
from mock import patch
from nose.tools import assert_equal, assert_true


@patch('centipede_ui.tickets.views.settings.CENTIPEDE_URL', 'http://centipede')
@patch('centipede_ui.centipedelib.requests.get')
def test_view_ticket(get):
    get.return_value.content = json.dumps({
        'title': 'Test Title',
        'description': 'Test Description',
        'owner': 'Test Owner',
        'state': 'Test State',
    })
    c = Client()
    response = c.get('/tickets/view/US123/')
    assert_equal(200, response.status_code)
    for string in ['Test Title', 'Test Description', 'Test Owner',
                   'Test State']:
        assert_true(string in response.content,
                        '"{0}" not on page'.format(string))
