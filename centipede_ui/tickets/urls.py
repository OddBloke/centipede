from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('centipede_ui.tickets.views',
    url(r'^view/(?P<ticket_id>.*)/$', 'view_ticket'),
)
