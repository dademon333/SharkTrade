import {bindActionCreators} from 'redux';

import RestAPI from './RestAPI';
import RestAPIErrors from './constants/RestAPIErrors';
import {store} from './Store';
import {accessTokenChanged, onlineChanged} from './slices/Global';
import {userDataChanged} from './slices/User';
import LocalStorage from './LocalStorage';
import WebSocketManager from './WebsocketManager';


class SystemFunctions {
    static _actions = bindActionCreators(
        {
            accessTokenChanged,
            userDataChanged,
            onlineChanged,
        },
        store.dispatch
    );

    static async connectBackend() {
        const accessToken = LocalStorage.getAccessToken();
        await WebSocketManager.init(accessToken);

        const currentOnline = await RestAPI.getCurrentOnline();
        // noinspection JSUnresolvedVariable
        if (currentOnline.current_online) {
            this._actions.onlineChanged(currentOnline.current_online);
        }

        if (accessToken == null) {
            return undefined;
        }
        await this.fetchUser(accessToken);
    }

    static async fetchUser(accessToken) {
        this._actions.accessTokenChanged(accessToken);
        const response = await RestAPI.getSelfInfo();

        if (!response.detail) {
            this._actions.userDataChanged(response);
        } else {
            this.handleAuthError(response.detail);
        }
    }

    static handleAuthError(detail) {
        switch (detail) {
            case RestAPIErrors.UNAUTHORIZED:
                LocalStorage.removeAccessToken();
                break;
            case RestAPIErrors.CONNECTION_ERROR:
                break;
            default:
                console.log('Unknown rest api error:', detail);
        }
    }
}

export default SystemFunctions;