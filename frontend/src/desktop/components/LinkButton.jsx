import {Component} from 'react';
import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';

import './scss/LinkButton.scss';


class LinkButton extends Component {
    render = () => {
        return (
            <Link to={this.props.to}>
                <button className="link-button">
                    {this.props.children}
                </button>
            </Link>
        )
    }
}

LinkButton.propTypes = {
    to: PropTypes.string.isRequired
}

export default LinkButton;