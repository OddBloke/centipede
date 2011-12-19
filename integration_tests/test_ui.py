import requests
from nose.tools import assert_true


def test_ui():
    # This test assumes the UI is running on http://127.0.0.1:8001 and is
    # configured to communicate with a Centipede instance configured with
    # Glasses Direct credentials.  It also assumes that US26 has not been
    # modified since the test was written.
    response = requests.get('http://127.0.0.1:8001/tickets/view/US26/')
    for string in ['Drop down nav', 'Accepted', "As product manager",
                   'I need to be able to change']:
        assert_true(string in response.content,
                    '"{0}" not on page.'.format(string))


def test_tasks():
    response = requests.get('http://127.0.0.1:8001/tickets/view/TA62/')
    for string in ['Document steps', 'Phil O', 'Completed']:
        assert_true(string in response.content,
                    '"{0}" not on page.'.format(string))
