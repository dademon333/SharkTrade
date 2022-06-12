import {connect} from 'react-redux';
import {useParams} from 'react-router-dom';

import DefaultModal from './DefaultModal';
import ModalErrorField from './components/ErrorField';
import ModalInput from './components/ModalInput';
import TextFunctions from '../../TextFunctions';
import RestAPIErrors from '../../constants/RestAPIErrors';
import RestAPI from '../../RestAPI';
import {modalChanged, screenSpinnerChanged} from '../../slices/Global';
import {lotPageLotDataChanged} from '../../slices/Content';


const CreateBidModal = (props) => {
    const {id: lotId} = useParams();
    const {
        open,
        user,
        screenSpinnerChanged,
        modalChanged,
        lotPageLotDataChanged
    } = props;

    const onSubmit = async (event) => {
        event.preventDefault();

        const errorField = document.querySelector('.rs-modal-content .modal__error-field');
        errorField.textContent = '';

        const amount = document.querySelector(
            '.rs-modal-content .modal__input[name="amount"]'
        ).value.trim();

        if (!TextFunctions.isNatural(amount)) {
            errorField.textContent = 'Это не похоже на число';
            return;
        }

        if (user.rublesBalance === null) {
            errorField.textContent = 'Сначала войдите в аккаунт';
            return;
        }

        if (user.rublesBalance < amount) {
            errorField.textContent = RestAPIErrors.TRANSLATIONS[RestAPIErrors.NOT_ENOUGH_MONEY];
            return;
        }

        screenSpinnerChanged(true);
        const response = await RestAPI.createBid(amount, lotId);
        if (!response.detail) {
            const lot = await RestAPI.getLot(lotId);
            lotPageLotDataChanged(lot);
            modalChanged(null);
        } else {
            errorField.textContent = RestAPIErrors.TRANSLATIONS[response.detail];
        }
        screenSpinnerChanged(false);
    }

    return (
        <DefaultModal
            title='Создание ставки'
            submitButtonText='Создать'
            open={open}
            onSubmit={onSubmit}
        >
            <ModalInput
                name="amount"
                placeholder="Сумма"
            />
            <ModalErrorField />
        </DefaultModal>
    )
}


const mapStateToProps = (state) => ({
    user: state.user
});

const mapDispatchToProps = {
    modalChanged,
    screenSpinnerChanged,
    lotPageLotDataChanged
}

export default connect(mapStateToProps, mapDispatchToProps)(CreateBidModal);