import requests
from nose.tools import assert_true


def test_ui():
    response = requests.get('http://127.0.0.1:8001/tickets/view/6/')
    for string in ['Work out how best to reflect', 'For example, owner',
                   'open']:
        assert_true(string in response.content,
                    '"{0}" not on page.'.format(string))
