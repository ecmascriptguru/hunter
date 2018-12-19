from django.urls import path, include

urlpatterns = [
    path('proxies', include(('email_hunter.apps.proxies.urls', 'email_hunter.apps.proxies'),
        namespace='proxies')),
    path('credentials/', include(('email_hunter.apps.credentials.urls', 'email_hunter.apps.credentials'),
        namespace='credentials')),
    path('targets/', include(('email_hunter.apps.targets.urls', 'email_hunter.apps.targets'),
        namespace='targets')),
    path('', include(('email_hunter.apps.users.urls', 'email_hunter.apps.users'), namespace='landings')),
]