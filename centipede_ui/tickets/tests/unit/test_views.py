from copy import deepcopy

from mock import Mock, patch
from nose.tools import assert_equal

from centipede_ui.tickets.views import view_ticket


@patch('centipede_ui.tickets.views.settings.CENTIPEDE_URL', 'MockURL')
@patch('centipede_ui.tickets.views.render_to_response')
@patch('centipede_ui.tickets.views.Centipede')
def test_view_ticket(centipede, render_to_response):
    ticket_dict = {
        'title': 'MockTitle',
        'description': 'MockDescription',
        'owner': 'MockOwner',
        'state': 'MockState',
        'identifier': 'MockIdentifier',
        }
    centipede.return_value.get_ticket.return_value = ticket_dict
    child_list = ['child1', 'child2']
    centipede.return_value.get_ticket_children.return_value = child_list
    ret = view_ticket(Mock(), 'US123')
    assert_equal([(('MockURL',), {})], centipede.call_args_list)
    assert_equal([(('US123',), {})],
                 centipede.return_value.get_ticket.call_args_list)
    expected_ticket_dict = deepcopy(ticket_dict)
    expected_ticket_dict['children'] = child_list
    assert_equal([(('tickets/view.html', expected_ticket_dict), {})],
                 render_to_response.call_args_list)
    assert_equal(render_to_response.return_value, ret)
