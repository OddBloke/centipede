from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('centipede.ui.tickets.views',
    url(r'^view/(?P<ticket_id>.*)/$', 'view_ticket'),
)
