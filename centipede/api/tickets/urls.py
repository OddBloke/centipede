from django.conf.urls.defaults import patterns, url

from centipede.api.tickets.views import TicketView


urlpatterns = patterns('',
    #url(r'^$', TicketListView.as_view()),
    url(r'^(?P<ticket_id>\w+)/$', TicketView.as_view()),
)
