import {Component} from 'react';
import {connect} from 'react-redux';

import './AuthPanel.scss';
import {accessTokenChanged, modalChanged} from '../../../slices/Global';
import Modals from '../../../constants/Modals';
import LocalStorage from '../../../LocalStorage';
import RestAPI from '../../../RestAPI';
import {userDataChanged} from '../../../slices/User';
import SystemFunctions from '../../../SystemFunctions';


class AuthPanel extends Component {
    onLogOut = async () => {
        LocalStorage.removeAccessToken();
        await RestAPI.logout();
        await SystemFunctions.connectBackend();
        this.props.userDataChanged(null);
        this.props.accessTokenChanged(null);
    }

    render = () => {
        if (this.props.user.id) {
            return (
                <div className="auth-panel">
                    <button
                        className="auth-panel__button auth-panel__logout-button"
                        onClick={async () => await this.onLogOut()}
                    >
                        Log out
                    </button>
                </div>
            )
        } else {
            return (
                <div className="auth-panel">
                    <button
                        className="auth-panel__button auth-panel__login-button"
                        onClick={() => this.props.modalChanged(Modals.LOG_IN)}
                    >
                        Log in
                    </button>
                    <button
                        className="auth-panel__button auth-panel__signup-button"
                        onClick={() => this.props.modalChanged(Modals.SIGN_UP)}
                    >
                        Sign up
                    </button>
                </div>
            )
        }

    }
}


const mapStateToProps = (state) => ({
    user: state.user
})

const mapDispatchToProps = {
    modalChanged,
    accessTokenChanged,
    userDataChanged
}

export default connect(mapStateToProps, mapDispatchToProps)(AuthPanel);