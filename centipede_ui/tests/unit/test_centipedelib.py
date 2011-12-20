from mock import patch
from mock_helpers import assert_called_once
from nose.tools import assert_equal, assert_raises

from centipede_ui.centipedelib import Centipede, DeadbeatTicket


@patch('centipede_ui.centipedelib.json.loads')
@patch('centipede_ui.centipedelib.requests.get')
def test_get_ticket(get, loads):
    centipede = Centipede('http://centipede')
    ret = centipede.get_ticket('US123')
    assert_called_once(get, ('http://centipede/tickets/US123/',))
    assert_equal([((get.return_value.content,), {})], loads.call_args_list)
    assert_equal(loads.return_value, ret)


@patch('centipede_ui.centipedelib.json.loads')
@patch('centipede_ui.centipedelib.requests.get')
def test_get_ticket_children(get, loads):
    get.return_value.status_code = 200
    centipede = Centipede('http://centipede')
    ret = centipede.get_ticket_children('US123')
    assert_called_once(get, ('http://centipede/tickets/US123/tickets/',))
    assert_equal([((get.return_value.content,), {})], loads.call_args_list)
    assert_equal(loads.return_value, ret)


@patch('centipede_ui.centipedelib.requests.get')
def test_get_ticket_children_unsupported(get):
    get.return_value.status_code = 404
    centipede = Centipede('http://centipede')
    assert_raises(DeadbeatTicket, centipede.get_ticket_children, 'US123')
