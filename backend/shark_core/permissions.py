from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)
from forum.permissions import (
    ThreadPermission,
    PostPermission
)
from steambot.permissions import (
    SteamBotQueuePermission
)

PERM_ALLOW_ANY = AllowAny
PERM_IS_AUTHENTICATED = IsAuthenticated
PERM_IS_ADMIN_USER = IsAdminUser
PERM_STEAMBOT_QUEUE = SteamBotQueuePermission
PERM_THREAD = ThreadPermission
PERM_POST = PostPermission
