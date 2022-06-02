import {Component} from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';

import {modalChanged} from '../../../slices/Global';
import '../scss/ModalButtons.scss';


class ModalButtons extends Component {
    render() {
        return (
            <div className='modal__buttons'>
                <button
                    type='button'
                    className='modal__button modal__cancel-button'
                    onClick={() => this.props.modalChanged(null)}
                >
                    Назад
                </button>
                <button
                    type='submit'
                    className={'modal__button modal__success-button'}
                >
                    {this.props.submitButtonText}
                </button>
            </div>
        )
    }
}
ModalButtons.propTypes = {
    submitButtonText: PropTypes.string
}

const mapDispatchToProps = {
    modalChanged
}

export default connect(undefined, mapDispatchToProps)(ModalButtons)