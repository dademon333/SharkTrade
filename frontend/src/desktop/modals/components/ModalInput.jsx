import {Component} from 'react';
import PropTypes from 'prop-types';

import '../scss/ModalInput.scss';


class ModalInput extends Component {
    render = () => {
        const {
            type,
            name,
            inputMode,
            placeholder,
        } = this.props;

        return (
            <input
                type={type || "text"}
                name={name}
                inputMode={inputMode}
                placeholder={placeholder}
                className="modal__input"
            />
        )
    }
}


ModalInput.propTypes = {
    type: PropTypes.string,
    name: PropTypes.string.isRequired,
    inputMode: PropTypes.string,
    placeholder: PropTypes.string.isRequired
}

export default ModalInput;