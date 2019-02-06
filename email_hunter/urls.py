from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('rs/proxies/', include(('email_hunter.apps.proxies.urls', 'email_hunter.apps.proxies'),
        namespace='proxies')),
    path('rs/credentials/', include(('email_hunter.apps.credentials.urls', 'email_hunter.apps.credentials'),
        namespace='credentials')),
    path('rs/jobs/', include(('email_hunter.apps.jobs.urls', 'email_hunter.apps.jobs'),
        namespace='jobs')),
    path('rs/', include(('email_hunter.apps.targets.urls', 'email_hunter.apps.targets'),
        namespace='targets')),
    path('st/leads/', include(('email_hunter.apps.leads.urls', 'email_hunter.apps.leads'),
        namespace='leads')),
    path('rs/', include(('email_hunter.apps.articles.urls', 'email_hunter.apps.articles'),
        namespace='articles')),
    path('', include(('email_hunter.apps.users.urls', 'email_hunter.apps.users'), namespace='landings')),
    path('api/', include(('email_hunter.apps.credentials.urls_api', 'email_hunter.apps.credentials'),
                                                namespace='credentials_api')),
    path('api/', include(('email_hunter.apps.proxies.urls_api', 'email_hunter.apps.proxies'),
                                                namespace='proxies_api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]