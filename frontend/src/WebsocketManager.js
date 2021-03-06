import {bindActionCreators} from 'redux';

import Config from './Config';
import {store} from './Store';
import {onlineChanged} from './slices/Global';
import WSMessageType from './constants/WSMessageType';


class WebsocketManager {
    static _socket;
    static _accessToken;

    static _actions = bindActionCreators(
        {
            onlineChanged
        },
        store.dispatch
    )

    static init = async (accessToken) => {
        this._accessToken = accessToken;
        if (this._socket) {
            await this._socket.close();
        }
        this._socket = await this._connectSocket();
    }

    static sendMessage = async (message) => {
        await this._socket.send(JSON.stringify(message));
    }

    static _handleMessage = (message) => {
        message = JSON.parse(message);

        switch (message.type) {
            case 'online_update':
                // noinspection JSUnresolvedVariable
                this._actions.onlineChanged(message.data.new_online);
                break;
            case 'auth_result':
                break;
            default:
                console.log('Unknown message type:', message);
        }
    }

    static _connectSocket = async () => {
        let serverUrl;
        if (Config.SERVER_URL.startsWith('https')) {
            serverUrl = Config.SERVER_URL.replace(/https/, 'wss') + '/ws/';
        } else {
            serverUrl = Config.SERVER_URL.replace(/http/, 'ws') + '/ws/';
        }

        const socket = new WebSocket(serverUrl);
        socket.addEventListener('message', (event) => this._handleMessage(event.data));
        socket.onopen = this._onOpen;
        socket.onclose = this._onClose;
        return socket;
    }

    static _onOpen = async () => {
        console.log('Socket connected');

        if (this._accessToken) {
            await this.sendMessage({
                type: WSMessageType.AUTH,
                access_token: this._accessToken
            })
        }
    }

    static _onClose = async (event) => {
        console.log('Socket disconnected');
        if (event.code === 3000) {
            this._accessToken = null;
        }
        if (event.code === 1005) {
            // Call close from frontend
            return;
        }
        await new Promise(r => setTimeout(r, 3000));
        await this._tryReconnect();
    }

    static _tryReconnect = async () => {
        this._socket = await this._connectSocket();
    }
}

export default WebsocketManager;