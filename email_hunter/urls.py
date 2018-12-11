from django.urls import path, include

urlpatterns = [
    path('proxies', include(('email_hunter.apps.proxies.urls', 'email_hunter.apps.proxies'),
        namespace='proxies')),
]