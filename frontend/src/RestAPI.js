import Config from './Config';
import RestAPIErrors from './constants/RestAPIErrors';
import {store} from './Store';


class RestAPI {
    static async handleError(error) {
        const body = await error.text();

        if (error.status === 500) {
            // Internal server error
            return {detail: RestAPIErrors.SERVER_ERROR};
        } else if (body) {
            // Server returned error description
            return JSON.parse(body);
        } else {
            // Unknown errors
            return error;
        }
    }

    static async _makeRequest(url, args) {
        args.signal = this._timeout(5000).signal;
        args.credentials = 'include'

        if(!args.headers) {
            args.headers = {}
        }

        const accessToken = store.getState().global.accessToken;
        if (accessToken) {
            args.headers['Authorization'] = `Bearer ${accessToken}`
        }

        if (args.json) {
            args.headers['Content-Type'] = 'application/json';
            args.body = JSON.stringify(args.json);
            delete args.json;
        }

        return await fetch(url, args)
            .then(async (response) => {
                if (response.ok) {
                    return await response.json();
                }
                return await this.handleError(response);
            })
            .catch(() => ({detail: RestAPIErrors.CONNECTION_ERROR}))
    }

    static _timeout (time) {
        let controller = new AbortController();
        setTimeout(() => controller.abort(), time);
        return controller;
    };


    static async login(username, password) {
        let formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        return await this._makeRequest(
            Config.SERVER_URL + '/login',
            {
                method: 'POST',
                body: formData
            }
        )
    }

    static async logout() {
        return await this._makeRequest(
            Config.SERVER_URL + '/logout',
            {method: 'DELETE'}
        )
    }

    static async signUp(email, username, password) {
        return await this._makeRequest(
            Config.SERVER_URL + '/api/users',
            {
                method: 'POST',
                json: {email, username, password}
            }
        )
    }


    static async getCurrentOnline() {
        return await this._makeRequest(
            Config.SERVER_URL + '/current_online',
            {method: 'GET'}
        )
    }

    static async getSelfInfo() {
        return await this._makeRequest(
            Config.SERVER_URL + '/api/users/me',
            {method: 'GET'}
        )
    }


    static async getAllLots(beforeId) {
        beforeId = beforeId ? `before_id=${beforeId}` : '';

        return await this._makeRequest(
            Config.SERVER_URL + `/api/lots/list?${beforeId}&limit=16`,
            {method: 'GET'}
        )
    }

    static async getOwnLots(beforeId) {
        beforeId = beforeId ? `before_id=${beforeId}` : '';

        return await this._makeRequest(
            Config.SERVER_URL + `/api/lots/my?${beforeId}&limit=16`,
            {method: 'GET'}
        )
    }

    static async getOwnBids(beforeId) {
        beforeId = beforeId ? `before_id=${beforeId}` : '';

        return await this._makeRequest(
            Config.SERVER_URL + `/api/bids/my?${beforeId}&limit=16`,
            {method: 'GET'}
        )
    }

    static async createBid(amount, lotId) {
        return await this._makeRequest(
            Config.SERVER_URL + `/api/bids/`,
            {
                method: 'POST',
                json: {amount, lot_id: lotId}
            }
        )
    }

    static async withdrawBid(bidId) {
        return await this._makeRequest(
            Config.SERVER_URL + `/api/bids/withdraw/${bidId}`,
            {method: 'POST'}
        )
    }

    static async getOwnItems(beforeId) {
        beforeId = beforeId ? `before_id=${beforeId}` : '';

        return await this._makeRequest(
            Config.SERVER_URL + `/api/items/my?${beforeId}&limit=16`,
            {method: 'GET'}
        )
    }

    static async getItem(lotId) {
        return await this._makeRequest(
            Config.SERVER_URL + `/api/items/${lotId}`,
            {method: 'GET'}
        )
    }


    static async getLot(lotId) {
        return await this._makeRequest(
            Config.SERVER_URL + `/api/lots/${lotId}`,
            {method: 'GET'}
        )
    }
}

export default RestAPI;