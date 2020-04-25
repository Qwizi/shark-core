export const CONFIG = {
    API: {
        URL: 'http://0.0.0.0:8000/api',
        ENDPOINTS: {
            TOKEN: {
                AUTH: '/auth/token/',
                REFRESH: '/auth/token/refresh/'
            },
            ACCOUNTS: {
                ME: '/accounts/me/',
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
            },
            NEWS: '/news/'
        },
    },
    STEAM: {
        OPENID_URL: 'https://steamcommunity.com/openid/login?',
        CALLBACK: '/auth/steam/callback/',
        REDIRECT: '/auh/steam/redirect/'
    }
};