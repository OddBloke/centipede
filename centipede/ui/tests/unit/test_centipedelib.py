from mock import patch
from nose.tools import assert_equal

from centipede.ui.centipedelib import Centipede


@patch('centipede.ui.centipedelib.json.loads')
@patch('centipede.ui.centipedelib.requests.get')
def test_get_ticket(get, loads):
    centipede = Centipede('http://centipede')
    ret = centipede.get_ticket('US123')
    assert_equal(1, get.call_count)
    args, kwargs = get.call_args
    assert_equal(('http://centipede/tickets/US123/',), args)
    assert_equal({}, kwargs)
    assert_equal([((get.return_value.content,), {})], loads.call_args_list)
    assert_equal(loads.return_value, ret)
