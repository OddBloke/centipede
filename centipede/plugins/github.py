from github2 import client

from centipede.tracker import TrackerInterface
from centipede.tracker.entities import IAmSterile, Ticket


def get_ticket_from_issue(issue):
    return Ticket(
        identifier=issue.number,
        description=issue.body,
        title=issue.title,
        owner=None,
        state=issue.state,
    )


class GitHub(TrackerInterface):

    def __init__(self, repo):
        self.repo = repo

    def get_ticket(self, ticket_id):
        github_lib = client.Github()
        issue = github_lib.issues.show(self.repo, ticket_id)
        return get_ticket_from_issue(issue)

    def list_children(self, ticket_id):
        raise IAmSterile('GitHub does not support nested issues.')

    def list_root(self):
        github_lib = client.Github()
        open_issues = github_lib.issues.list()
        closed_issues = github_lib.issues.list(state='closed')
        ret = []
        for issue in open_issues + closed_issues:
            ret.append(get_ticket_from_issue(issue))
        return ret


class GitHubWithSettings(GitHub):

    def __init__(self, settings):
        self.repo = settings.GITHUB_REPO
