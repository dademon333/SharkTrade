class LocalStorage {
    static getAccessToken() {
        return localStorage.getItem('accessToken');
    }

    static setAccessToken(accessToken) {
        return localStorage.setItem('accessToken', accessToken);
    }

    static removeAccessToken() {
        return localStorage.removeItem('accessToken');
    }
}

export default LocalStorage;