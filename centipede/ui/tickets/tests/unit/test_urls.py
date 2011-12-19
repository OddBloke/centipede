from django.core.urlresolvers import resolve
from nose.tools import assert_equal

from centipede.ui.tickets import views


def test_view_ticket():
    assert_equal(views.view_ticket.func_code,
                 resolve('/tickets/view/US123/').func.func_code)
