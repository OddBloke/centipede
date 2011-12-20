from mock import Mock, patch
from mock_helpers import assert_called_once, MultiReturn
from nose.tools import assert_equal, assert_raises, assert_true

from centipede.plugins.github import (
    get_ticket_from_issue,
    GitHub,
    GitHubWithSettings,
)
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


@patch('centipede.plugins.github.client.Github')
@patch('centipede.plugins.github.get_ticket_from_issue')
def test_list_root(get_ticket_from_issue, github_lib):
    get_ticket_from_issue.side_effect = lambda x: x + 100
    issue_list = github_lib.return_value.issues.list
    issue_list.side_effect = MultiReturn([[1,2], [3,4]]).side_effect
    github = GitHub('MockUser/MockRepo')
    ret = github.list_root()
    assert_called_once(github_lib)
    assert_equal(2, issue_list.call_count)
    expected_kwargs = [{}, {'state': 'closed'}]
    for args, kwargs in issue_list.call_args_list:
        assert_equal((), args)
        assert_true(kwargs in expected_kwargs)
        expected_kwargs.remove(kwargs)
    assert_equal(4, get_ticket_from_issue.call_count)
    get_ticket_from_issue_args = [
            call[0][0] for call in get_ticket_from_issue.call_args_list]
    assert_equal(set([1,2,3,4]), set(get_ticket_from_issue_args))
    assert_equal(set([101,102,103,104]), set(ret))


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
