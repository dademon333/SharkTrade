import {bindActionCreators} from 'redux';

import RestAPI from './RestAPI';
import RestAPIErrors from './constants/RestAPIErrors';
import {store} from './Store';
import {accessTokenChanged} from './slices/Global';
import {userDataChanged} from './slices/User';
import LocalStorage from './LocalStorage';


class SystemFunctions {
    static _actions = bindActionCreators(
        {
            accessTokenChanged,
            userDataChanged,
        },
        store.dispatch
    );

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