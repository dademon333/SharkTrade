import {Component} from 'react';
import {connect} from 'react-redux';
import {modalChanged} from '../../slices/Global';
import {Modal} from 'rsuite';
import PropTypes from 'prop-types';

import ModalButtons from './components/ModalButtons';


class DefaultModal extends Component {
    componentDidUpdate = () => {
        const form = document.querySelector('.modal__form');
        if (form === null) {
            return undefined;
        }
        form.addEventListener('submit', this.props.onSubmit);
    }

    render = () => {
        const {
            open,
            title,
            size,
            submitButtonText
        } = this.props;

        return (
            <Modal
                open={open}
                size={size || 'xs'}
                onClose={() => this.props.modalChanged(null)}
            >
                <Modal.Header>
                    <Modal.Title>{title}</Modal.Title>
                </Modal.Header>
                <div className="modal__body">
                    <form action={'#'} className="modal__form">
                        {this.props.children}
                        <ModalButtons submitButtonText={submitButtonText}/>
                    </form>
                </div>
            </Modal>
        )
    }
}


DefaultModal.propTypes = {
    open: PropTypes.bool.isRequired,
    title: PropTypes.string.isRequired,
    size: PropTypes.string,
    onSubmit: PropTypes.func.isRequired,
    submitButtonText: PropTypes.string
}

const mapDispatchToProps = {
    modalChanged: modalChanged
}

export default connect(null, mapDispatchToProps)(DefaultModal);