from pyrally import RallyAPIClient, settings as rally_settings

from centipede.tracker import TrackerInterface
from centipede.tracker.entities import IAmSterile, Ticket


def get_ticket_from_rally_object(rally_obj):
    owner = rally_obj.Owner
    if owner is not None:
        owner = owner.DisplayName
    try:
        state = rally_obj.ScheduleState
    except AttributeError:
        state = rally_obj.State
    return Ticket(
            identifier=rally_obj.FormattedID,
            description=rally_obj.Description,
            title=rally_obj.Name,
            owner=owner,
            state=state,
        )


class Rally(TrackerInterface):

    def __init__(self, settings=None):
        self.client = RallyAPIClient(rally_settings.RALLY_USERNAME,
                                     rally_settings.RALLY_PASSWORD)

    def get_ticket(self, ticket_id):
        ticket = self.client.get_entity_by_name(ticket_id)
        return get_ticket_from_rally_object(ticket)

    def list_children(self, ticket_id):
        ticket = self.client.get_entity_by_name(ticket_id)
        if not (hasattr(ticket, 'children') or hasattr(ticket, 'tasks')):
            raise IAmSterile(ticket)
        try:
            children = [get_ticket_from_rally_object(child)
                            for child in ticket.children]
        except AttributeError:
            children = []
        tasks = [get_ticket_from_rally_object(task) for task in ticket.tasks]
        return children + tasks

    def list_root(self):
        entities = self.client.get_all_entities()
        return [get_ticket_from_rally_object(entity) for entity in entities]
