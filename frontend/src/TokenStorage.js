class TokenStorage {
    setAccessToken(token) {
        localStorage.setItem('access_token', token);
    }

    getAccessToken() {
        return localStorage.getItem('access_token');
    }

    setRefreshToken(token) {
        localStorage.setItem('refresh_token', token)
    }

    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    setTokens(access, refresh) {
        this.setAccessToken(access);
        this.setRefreshToken(refresh);
    }

    removeAccessToken() {
        localStorage.removeItem('access_token');
    }

    removeRefreshToken() {
        localStorage.removeItem('refresh_token');
    }

    removeTokens() {
        this.removeAccessToken();
        this.removeRefreshToken();
    }
}

export const tokenStorage = new TokenStorage;

