from mock import Mock, patch
from nose.tools import assert_equal, assert_raises

from centipede.plugins.github import (
    get_ticket_from_issue,
    GitHub,
    GitHubWithSettings,
)
from centipede.plugins.tests.unit.test_rally import assert_called_once
from centipede.tracker.entities import IAmSterile


@patch('centipede.plugins.github.client.Github')
@patch('centipede.plugins.github.get_ticket_from_issue')
def test_get_ticket(get_ticket_from_issue, github_lib):
    github = GitHub('MockUser/MockRepo')
    ret = github.get_ticket('MockTicketNumber')
    assert_called_once(github_lib)
    assert_called_once(github_lib.return_value.issues.show,
                        ('MockUser/MockRepo', 'MockTicketNumber'))
    assert_called_once(
        get_ticket_from_issue,
        (github_lib.return_value.issues.show.return_value,), {})
    assert_equal(get_ticket_from_issue.return_value, ret)


def test_list_children():
    github = GitHub('')
    assert_raises(IAmSterile, github.list_children, '2')


@patch('centipede.plugins.github.Ticket')
def test_get_ticket_from_issue(ticket):
    issue = Mock(['body', 'number', 'state', 'title'])
    issue.body = 'MockBody'
    issue.number = 123
    issue.state = 'MockState'
    issue.title = 'MockTitle'
    ret = get_ticket_from_issue(issue)
    assert_called_once(ticket, (), {
        'identifier': 123,
        'description': 'MockBody',
        'title': 'MockTitle',
        'owner': None,
        'state': 'MockState',
    })
    assert_equal(ticket.return_value, ret)


def test_github_with_settings():
    settings = Mock()
    settings.GITHUB_REPO = 'MockRepo'
    gh = GitHubWithSettings(settings)
    assert_equal('MockRepo', gh.repo)
