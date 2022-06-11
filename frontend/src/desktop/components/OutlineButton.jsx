import {Component} from 'react';
import PropTypes from 'prop-types';

import './scss/OutlineButton.scss';


class OutlineButton extends Component {
    render = () => {
        return (
            <button
                className="outline-button"
                onClick={this.props.onClick}
            >
                {this.props.children}
            </button>
        )
    }
}


OutlineButton.propTypes = {
    onClick: PropTypes.func
}

export default OutlineButton;