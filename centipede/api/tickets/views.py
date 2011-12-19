import anyjson
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

from centipede.tracker import load_tracker


tracker = load_tracker(settings.TRACKER)


class TicketView(View):

    def serialize(self, data):
        return anyjson.serialize(data)

    def get(self, request, ticket_id):
        ticket = tracker.get_ticket(ticket_id)
        data = dict(
            title=ticket.title,
            description=ticket.description,
            state=ticket.state,
            owner=ticket.owner)
        return HttpResponse(self.serialize(data))
