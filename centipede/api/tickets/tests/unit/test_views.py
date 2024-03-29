from mock import Mock, patch
from mock_helpers import assert_called_once
from nose.tools import assert_equal

from centipede.api.tickets.views import TicketChildView, TicketView
from centipede.tracker.entities import IAmSterile


@patch('centipede.api.tickets.views.HttpResponse')
@patch('centipede.api.tickets.views.tracker')
@patch('centipede.api.tickets.views.anyjson.serialize')
def test_ticketchildview(serialize, tracker, response):
    children = [Mock(), Mock()]
    tracker.list_children.return_value = children
    ret = TicketChildView().get(Mock(), 'US123')
    assert_called_once(tracker.list_children, ('US123',))
    assert_called_once(serialize,
                       ([c.as_dict.return_value for c in children],))
    assert_called_once(response, (serialize.return_value,))
    assert_equal(response.return_value, ret)


@patch('centipede.api.tickets.views.tracker')
@patch('centipede.api.tickets.views.anyjson.serialize')
def test_ticketchildview_sterile(serialize, tracker):
    tracker.list_children.side_effect = IAmSterile
    ret = TicketChildView().get(Mock(), 'US123')
    assert_called_once(tracker.list_children, ('US123',))
    assert_equal(0, serialize.call_count)
    assert_equal(404, ret.status_code)
    assert_equal('', ret.content)



@patch('centipede.api.tickets.views.HttpResponse')
@patch('centipede.api.tickets.views.tracker')
@patch('centipede.api.tickets.views.anyjson.serialize')
def test_ticketview(serialize, tracker, response):
    ret = TicketView().get(Mock(), 'US123')
    assert_called_once(tracker.get_ticket, ('US123',))
    assert_called_once(serialize,
                       (tracker.get_ticket.return_value.as_dict.return_value,))
    assert_called_once(response, (serialize.return_value,))
    assert_equal(response.return_value, ret)
