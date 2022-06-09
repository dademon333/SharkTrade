import {Component} from 'react';
import PropTypes from 'prop-types';

import DefaultModal from './DefaultModal';
import ModalInput from './components/ModalInput';
import ModalErrorField from './components/ErrorField';
import RestAPI from '../../RestAPI';
import RestAPIErrors from '../../constants/RestAPIErrors';
import SystemFunctions from '../../SystemFunctions';
import {modalChanged, screenSpinnerChanged} from '../../slices/Global';
import {connect} from 'react-redux';
import LocalStorage from '../../LocalStorage';


class LogInModal extends Component {
    onSubmit = async (event) => {
        event.preventDefault();

        const errorField = document.querySelector('.rs-modal-content .modal__error-field');
        errorField.textContent = '';

        const username = document.querySelector(
            '.rs-modal-content .modal__input[name="username"]'
        ).value.trim();
        const password = document.querySelector(
            '.rs-modal-content .modal__input[name="password"]'
        ).value.trim();

        if (!username) {
            errorField.textContent = 'Введите никнейм';
            return;
        }
        if (!password) {
            errorField.textContent = 'Введите пароль';
            return;
        }

        this.props.screenSpinnerChanged(true);
        const response = await RestAPI.login(username, password);
        if (!response.detail) {
            // noinspection JSUnresolvedVariable
            const accessToken = response.access_token;
            LocalStorage.setAccessToken(accessToken);
            await SystemFunctions.connectBackend(accessToken);
            this.props.modalChanged(null);
        } else {
            errorField.textContent = RestAPIErrors.TRANSLATIONS[response.detail];
        }
        this.props.screenSpinnerChanged(false);
    }

    render = () => {
        return (
            <DefaultModal
                title='Войти'
                submitButtonText='Войти'
                open={this.props.open}
                onSubmit={this.onSubmit}
            >
                <ModalInput
                    name="username"
                    placeholder="Никнейм или почта"
                />
                <ModalInput
                    type="password"
                    name="password"
                    placeholder="Пароль"
                />
                <ModalErrorField />
            </DefaultModal>
        )
    }
}


LogInModal.propTypes = {
    open: PropTypes.bool.isRequired
}

const mapDispatchToProps = {
    modalChanged,
    screenSpinnerChanged
}

export default connect(null, mapDispatchToProps)(LogInModal);