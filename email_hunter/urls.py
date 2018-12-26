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
    path('', include(('email_hunter.apps.users.urls', 'email_hunter.apps.users'), namespace='landings')),
]