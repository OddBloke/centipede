from github2 import client

from centipede.tracker import TrackerInterface


def get_ticket_from_issue():
    pass


class GitHub(TrackerInterface):

    def get_ticket(self, ticket_id):
        github_lib = client.Github()
        issue = github_lib.issues.show('MockPerson/MockRepo', ticket_id)
        ticket = get_ticket_from_issue(issue)
        return ticket
