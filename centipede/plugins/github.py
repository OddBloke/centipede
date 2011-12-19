from github2 import client

from centipede.tracker import TrackerInterface
from centipede.tracker.entities import Ticket


def get_ticket_from_issue(issue):
    return Ticket(
        identifier=issue.number,
        description=issue.body,
        title=issue.title,
        owner=None,
        state=issue.state,
    )


class GitHub(TrackerInterface):

    def get_ticket(self, ticket_id):
        github_lib = client.Github()
        issue = github_lib.issues.show('MockPerson/MockRepo', ticket_id)
        return get_ticket_from_issue(issue)
