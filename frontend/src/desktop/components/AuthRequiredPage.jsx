import {Component} from 'react';

import WonderPersikPage from './WonderPersikPage';
import OutlineButton from './OutlineButton';
import Modals from '../../constants/Modals';
import {modalChanged} from '../../slices/Global';
import {connect} from 'react-redux';


class AuthRequiredPage extends Component {
    render = () => {
        return (
            <WonderPersikPage>
                Для доступа к этому разделу нужно войти в свой аккаунт
                <OutlineButton onClick={() => this.props.modalChanged(Modals.LOG_IN)}>
                    Войти
                </OutlineButton>
            </WonderPersikPage>
        )
    }
}


const mapDispatchToProps = {
    modalChanged
}

export default connect(null, mapDispatchToProps)(AuthRequiredPage);