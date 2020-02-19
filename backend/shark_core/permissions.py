from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)
from steambot.permissions import (
    SteamBotQueuePermission
)

PERM_ALLOW_ANY = AllowAny
PERM_IS_AUTHENTICATED = IsAuthenticated
PERM_IS_ADMIN_USER = IsAdminUser
PERM_STEAMBOT_QUEUE = SteamBotQueuePermission
