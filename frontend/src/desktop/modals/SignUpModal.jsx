import PropTypes from 'prop-types';
import {Component} from 'react';
import {connect} from 'react-redux';

import DefaultModal from './DefaultModal';
import ModalErrorField from './components/ErrorField';
import {modalChanged, screenSpinnerChanged} from '../../slices/Global';
import ModalInput from './components/ModalInput';
import RestAPI from '../../RestAPI';
import SystemFunctions from '../../SystemFunctions';
import LocalStorage from '../../LocalStorage';
import RestAPIErrors from '../../constants/RestAPIErrors';


class SignUpModal extends Component {
    onSubmit = async (event) => {
        event.preventDefault();

        const errorField = document.querySelector('.rs-modal-content .modal__error-field');
        errorField.textContent = '';

        const email = document.querySelector(
            '.rs-modal-content .modal__input[name="email"]'
        ).value.trim();
        const username = document.querySelector(
            '.rs-modal-content .modal__input[name="username"]'
        ).value.trim();
        const password = document.querySelector(
            '.rs-modal-content .modal__input[name="password"]'
        ).value.trim();

        if (!email) {
            errorField.textContent = 'Введите почту';
            return;
        }
        if (!username) {
            errorField.textContent = 'Введите никнейм';
            return;
        }
        if (!password) {
            errorField.textContent = 'Введите пароль';
            return;
        }

        this.props.screenSpinnerChanged(true);
        const response = await RestAPI.signUp(email, username, password);
        if (!response.detail) {
            // noinspection JSUnresolvedVariable
            const accessToken = response.access_token;
            LocalStorage.setAccessToken(accessToken);
            await SystemFunctions.connectBackend(accessToken);
            this.props.modalChanged(null);
        } else {
            let errorDescription;
            if (RestAPIErrors.TRANSLATIONS[response.detail]) {
                errorDescription = response.detail;
            } else {
                const location = response.detail[0]?.loc
                const field = location?.[location.length - 1];

                if (field === 'email') {
                    errorDescription = RestAPIErrors.INVALID_EMAIL;
                } else if (field === 'username') {
                    errorDescription = RestAPIErrors.INVALID_USERNAME;
                } else if (field === 'password') {
                    errorDescription = RestAPIErrors.INVALID_PASSWORD;
                } else {
                    errorDescription = RestAPIErrors.UNKNOWN_ERROR;
                    console.log('Unknown rest api error:', response.detail);
                }
            }
            errorField.textContent = RestAPIErrors.TRANSLATIONS[errorDescription];
        }
        this.props.screenSpinnerChanged(false);
    }

    render = () => {
        return (
            <DefaultModal
                title='Присоединиться'
                submitButtonText='Присоединиться'
                open={this.props.open}
                onSubmit={this.onSubmit}
            >
                <ModalInput
                    name="email"
                    type="email"
                    placeholder="Почта"
                />
                <ModalInput
                    name="username"
                    placeholder="Никнейм"
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


SignUpModal.propTypes = {
    open: PropTypes.bool.isRequired
}

const mapDispatchToProps = {
    modalChanged,
    screenSpinnerChanged
}

export default connect(null, mapDispatchToProps)(SignUpModal);