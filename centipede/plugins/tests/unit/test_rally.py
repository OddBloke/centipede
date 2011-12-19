from mock import patch
from nose.tools import assert_equal

from centipede.plugins.rally import Rally


@patch('centipede.plugins.rally.RallyAPIClient')
def test_rally_get(api_client):
    rally = Rally()
    rally.get('us123')
    get_story_by_name = api_client.return_value.get_story_by_name
    assert_equal(1, get_story_by_name.call_count)
    args, kwargs = get_story_by_name.call_args
    assert_equal(('us123',), args)
    assert_equal({}, kwargs)
