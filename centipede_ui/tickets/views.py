from django.conf import settings
from django.shortcuts import render_to_response

from centipede_ui.centipedelib import Centipede, DeadbeatTicket


def view_ticket(request, ticket_id):
    centipede = Centipede(settings.CENTIPEDE_URL)
    ticket_dict = centipede.get_ticket(ticket_id)
    try:
        ticket_dict['children'] = centipede.get_ticket_children(ticket_id)
    except DeadbeatTicket:
        pass
    return render_to_response('tickets/view.html', ticket_dict)
