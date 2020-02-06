export const CONFIG = {
    API: {
        URL: 'http://0.0.0.0:8000/api',
        ENDPOINTS: {
            TOKEN: {
                AUTH: '/auth/token/',
                REFRESH: '/token/refresh/'
            },
            FORUM: {
                CATEGORIES: '/forum/categories/',
                THREADS: '/forum/threads/',
                POSTS: '/forum/posts/'
            },
            SOURCEMOD: {
                SERVERS: '/sourcemod/servers/',
                ADMINS: '/sourcemod/admins/'
            },
            STORE: {
                CATEGORIES: '/store/categories/',
                BONUSES: '/store/bonuses/'
            }
        },
    },
    STEAM: {
        CALLBACK: '/steam_callback/'
    }
};