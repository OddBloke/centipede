from django.conf import settings
from django.shortcuts import render_to_response

from centipede_ui.centipedelib import Centipede


def view_ticket(request, ticket_id):
    centipede = Centipede(settings.CENTIPEDE_URL)
    ticket_dict = centipede.get_ticket(ticket_id)
    return render_to_response('tickets/view.html', ticket_dict)
