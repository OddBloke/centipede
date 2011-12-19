from mock import patch
from nose.tools import assert_equal

from centipede.plugins.rally import Rally


def assert_called_once(mock_obj, expected_args=None, expected_kwargs=None):
    if expected_args is None:
        expected_args = ()
    if expected_kwargs is None:
        expected_kwargs = {}
    assert_equal(1, mock_obj.call_count)
    args, kwargs = mock_obj.call_args
    assert_equal(expected_args, args)
    assert_equal(expected_kwargs, kwargs)


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_rally_get(api_client, get_ticket_from_rally_object):
    rally = Rally()
    ret = rally.get('us123')
    get_story_by_name = api_client.return_value.get_story_by_name
    assert_called_once(get_story_by_name, ('us123',))
    assert_called_once(get_ticket_from_rally_object,
                       (get_story_by_name.return_value,))
    assert_equal(get_ticket_from_rally_object.return_value, ret)
