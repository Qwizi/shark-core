from django.urls import path, include
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import AccountAuthSteamTokenView, ServerAccountAuthSteamTokenView

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', include('adminapi.urls')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/token/', AccountAuthSteamTokenView.as_view()),
    path('auth/server/token/', ServerAccountAuthSteamTokenView.as_view()),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('store/', include('store.urls')),
    path('forum/', include('forum.urls')),
    path('sourcemod/', include('smadmins.urls')),
    path('sourcemod/', include('servers.urls')),
    path('steambot/', include('steambot.urls', namespace='steambot'))
]
