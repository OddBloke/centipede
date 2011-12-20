from django.core.urlresolvers import resolve
from nose.tools import assert_equal

from centipede.api.tickets import views


def test_view_ticket():
    assert_equal(views.TicketView.as_view().func_code,
                 resolve('/tickets/US123/').func.func_code)


def test_view_ticket_children():
    assert_equal(views.TicketChildView.as_view().func_code,
                 resolve('/tickets/US123/tickets/').func.func_code)
