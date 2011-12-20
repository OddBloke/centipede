import anyjson
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

from centipede.tracker import load_tracker
from centipede.tracker.entities import IAmSterile


tracker = load_tracker(settings.TRACKER)


class TicketChildView(View):

    def get(self, request, ticket_id):
        try:
            children = tracker.list_children(ticket_id)
        except IAmSterile:
            return HttpResponse(status=404)
        return HttpResponse(anyjson.serialize(
            [ticket.as_dict() for ticket in children]))


class TicketView(View):

    def get(self, request, ticket_id):
        ticket = tracker.get_ticket(ticket_id)
        return HttpResponse(anyjson.serialize(ticket.as_dict()))
