from mock import Mock, patch
from mock_helpers import assert_called_once
from nose.tools import assert_equal, assert_raises

from centipede.tracker.entities import IAmSterile
from centipede.plugins.rally import get_ticket_from_rally_object, Rally


def _get_mock_entity(state_key='ScheduleState'):
    mock_rally_obj = Mock(['FormattedID', 'Description', 'Name', 'Owner',
                           state_key])
    mock_rally_obj.FormattedID = 'Mock Identifier'
    mock_rally_obj.Description = 'MockDescription'
    mock_rally_obj.Name = 'MockTitle'
    mock_rally_obj.Owner.DisplayName = 'Mock User'
    setattr(mock_rally_obj, state_key, 'Completed')
    return mock_rally_obj


@patch('centipede.plugins.rally.Ticket')
def test_get_ticket_from_rally_object(ticket):
    mock_rally_obj = _get_mock_entity()
    ret = get_ticket_from_rally_object(mock_rally_obj)
    assert_called_once(ticket, (), {
        'identifier': 'Mock Identifier',
        'description': 'MockDescription',
        'title': 'MockTitle',
        'owner': 'Mock User',
        'state': 'Completed',
    })
    assert_equal(ret, ticket.return_value)


@patch('centipede.plugins.rally.Ticket')
def test_get_ticket_from_rally_object_state(ticket):
    mock_rally_obj = _get_mock_entity('State')
    get_ticket_from_rally_object(mock_rally_obj)
    assert_called_once(ticket, (), {
        'identifier': 'Mock Identifier',
        'description': 'MockDescription',
        'title': 'MockTitle',
        'owner': 'Mock User',
        'state': 'Completed',
    })


@patch('centipede.plugins.rally.Ticket')
def test_get_ticket_from_rally_object_no_owner(ticket):
    mock_rally_obj = Mock()
    mock_rally_obj.Owner = None
    get_ticket_from_rally_object(mock_rally_obj)
    assert_equal(1, ticket.call_count)
    assert_equal(None, ticket.call_args[1]['owner'])


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_rally_get_ticket(api_client, get_ticket_from_rally_object):
    rally = Rally()
    ret = rally.get_ticket('us123')
    get_entity_by_name = api_client.return_value.get_entity_by_name
    assert_called_once(get_entity_by_name, ('us123',))
    assert_called_once(get_ticket_from_rally_object,
                       (get_entity_by_name.return_value,))
    assert_equal(get_ticket_from_rally_object.return_value, ret)


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_list_children_story_with_only_children(api_client,
                                                get_ticket_from_rally_object):
    rally = Rally()
    get_ticket_from_rally_object.side_effect = lambda x: x + 100
    get_entity_by_name = api_client.return_value.get_entity_by_name
    get_entity_by_name.return_value.children = [1, 2, 3]
    get_entity_by_name.return_value.tasks = []
    ret = rally.list_children('us123')
    assert_called_once(get_entity_by_name, ('us123',))
    assert_equal([101, 102, 103], ret)


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_list_children_entity_with_only_tasks(api_client,
                                              get_ticket_from_rally_object):
    rally = Rally()
    get_ticket_from_rally_object.side_effect = lambda x: x + 100
    get_entity_by_name = api_client.return_value.get_entity_by_name
    get_entity_by_name.return_value.children = []
    get_entity_by_name.return_value.tasks = [1, 2, 3]
    ret = rally.list_children('us123')
    assert_called_once(get_entity_by_name, ('us123',))
    assert_equal([101, 102, 103], ret)


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_list_children_entity_with_both(api_client,
                                        get_ticket_from_rally_object):
    rally = Rally()
    get_ticket_from_rally_object.side_effect = lambda x: x + 100
    get_entity_by_name = api_client.return_value.get_entity_by_name
    get_entity_by_name.return_value.children = [1, 2, 3]
    get_entity_by_name.return_value.tasks = [4, 5, 6]
    ret = rally.list_children('us123')
    assert_called_once(get_entity_by_name, ('us123',))
    assert_equal(set([101, 102, 103, 104, 105, 106]), set(ret))


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_list_children_defect(api_client, get_ticket_from_rally_object):
    rally = Rally()
    get_ticket_from_rally_object.side_effect = lambda x: x + 100
    get_entity_by_name = api_client.return_value.get_entity_by_name
    get_entity_by_name.return_value = Mock(['tasks'])
    get_entity_by_name.return_value.tasks = []
    ret = rally.list_children('de123')
    assert_called_once(get_entity_by_name, ('de123',))
    assert_equal([], ret)


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_list_children_task(api_client, get_ticket_from_rally_object):
    rally = Rally()
    get_ticket_from_rally_object.side_effect = lambda x: x + 100
    get_entity_by_name = api_client.return_value.get_entity_by_name
    get_entity_by_name.return_value = Mock([])
    assert_raises(IAmSterile, rally.list_children, 'ta123')
    assert_called_once(get_entity_by_name, ('ta123',))


@patch('centipede.plugins.rally.get_ticket_from_rally_object')
@patch('centipede.plugins.rally.RallyAPIClient')
def test_list_root(api_client, get_ticket_from_rally_object):
    def _create_mock(n, testcase=False):
        m = Mock()
        m.num = n
        if testcase:
            m._type = 'TestCase'
        return m
    rally = Rally()
    get_ticket_from_rally_object.side_effect = lambda x: x.num + 100
    api_client.return_value.get_all_entities.return_value = [
            _create_mock(1),
            _create_mock(2, True),
            _create_mock(3),
            _create_mock(4, True),
            _create_mock(5)]
    ret = rally.list_root()
    assert_equal([101, 103, 105], ret)
