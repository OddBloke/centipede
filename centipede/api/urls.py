from django.conf.urls.defaults import patterns, include

from centipede.api.tickets.views import TicketView


urlpatterns = patterns('',
    (r'^tickets/', include('centipede.api.tickets.urls')),
)
