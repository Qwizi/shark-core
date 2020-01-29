export const CONFIG = {
    API: {
        URL: 'http://localhost:8000/api',
        ENDPOINTS: {
            TOKEN: {
                AUTH: '/token/auth/',
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