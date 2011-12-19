from django.core.urlresolvers import resolve
from nose.tools import assert_equal

from centipede.api.tickets.views import TicketView

def test_ticket_URL():
    """Test the ticket resource URL."""
    match = resolve('/tickets/XXX/')
    assert_equal(TicketView.as_view(), match.func)
