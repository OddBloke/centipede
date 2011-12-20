import anyjson
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

from centipede.tracker import load_tracker


tracker = load_tracker(settings.TRACKER)


class TicketChildView(View):

    def get(self, request, ticket_id):
        children = tracker.list_children(ticket_id)
        return HttpResponse(anyjson.serialize(
            [ticket.as_dict() for ticket in children]))


class TicketView(View):

    def serialize(self, data):
        return anyjson.serialize(data)

    def get(self, request, ticket_id):
        ticket = tracker.get_ticket(ticket_id)
        return HttpResponse(self.serialize(ticket.as_dict()))
