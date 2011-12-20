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
        return json.loads(response.content)
