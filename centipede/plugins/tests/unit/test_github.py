from mock import patch
from nose.tools import assert_equal

from centipede.plugins.github import GitHub
from centipede.plugins.tests.unit.test_rally import assert_called_once


@patch('centipede.plugins.github.client.Github')
@patch('centipede.plugins.github.get_ticket_from_issue')
def test_get_ticket(get_ticket_from_issue, github_lib):
    github = GitHub()
    ret = github.get_ticket('MockTicketNumber')
    assert_called_once(github_lib)
    assert_called_once(github_lib.return_value.issues.show,
                        ('MockPerson/MockRepo', 'MockTicketNumber'))
    assert_called_once(
        get_ticket_from_issue,
        (github_lib.return_value.issues.show.return_value,), {})
    assert_equal(get_ticket_from_issue.return_value, ret)
