import json

import requests


def urljoin(*args):
    return '/'.join([arg.strip('/') for arg in args]) + '/'


class Centipede(object):

    def __init__(self, url):
        self.url = url

    def get_ticket(self, ticket_id):
        response = requests.get(urljoin(self.url, 'tickets', ticket_id))
        return json.loads(response.content)

    def get_ticket_children(self, ticket_id):
        response = requests.get(urljoin(self.url, 'tickets', ticket_id,
                                        'tickets'))
        if response.status_code == 200:
            return json.loads(response.content)
        elif response.status_code == 404:
            raise DeadbeatTicket(response)


class DeadbeatTicket(Exception):
    """Ticket does not support children."""
    pass
