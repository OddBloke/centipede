from mock import Mock, patch
from nose.tools import assert_equal

from centipede.plugins.rally import get_ticket_from_rally_object, Rally


def assert_called_once(mock_obj, expected_args=None, expected_kwargs=None):
    if expected_args is None:
        expected_args = ()
    if expected_kwargs is None:
        expected_kwargs = {}
    assert_equal(1, mock_obj.call_count)
    args, kwargs = mock_obj.call_args
    assert_equal(expected_args, args)
    assert_equal(expected_kwargs, kwargs)


@patch('centipede.plugins.rally.Ticket')
def test_get_ticket_from_rally_object(ticket):
    mock_rally_obj = Mock()
    mock_rally_obj.Description = 'MockDescription'
    mock_rally_obj.Name = 'MockTitle'
    mock_rally_obj.Owner.DisplayName = 'Mock User'
    mock_rally_obj.ScheduleState = 'Completed'
    ret = get_ticket_from_rally_object(mock_rally_obj)
    assert_called_once(ticket, (), {
        'description': 'MockDescription',
        'title': 'MockTitle',
        'owner': 'Mock User',
        'state': 'Completed',
    })
    assert_equal(ret, ticket.return_value)


@patch('centipede.plugins.rally.Ticket')
def test_get_ticket_from_rally_object_no_owner(ticket):
    mock_rally_obj = Mock()
    mock_rally_obj.Owner = None
    get_ticket_from_rally_object(mock_rally_obj)
    assert_equal(1, ticket.call_count)
    assert_equal(None, ticket.call_args[1]['owner'])


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_rally_get(api_client, get_ticket_from_rally_object):
    rally = Rally()
    ret = rally.get('us123')
    get_entity_by_name = api_client.return_value.get_entity_by_name
    assert_called_once(get_entity_by_name, ('us123',))
    assert_called_once(get_ticket_from_rally_object,
                       (get_entity_by_name.return_value,))
    assert_equal(get_ticket_from_rally_object.return_value, ret)
