import {Component} from 'react';
import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';

import OutlineButton from './OutlineButton';


class LinkButton extends Component {
    render = () => {
        return (
            <Link to={this.props.to}>
                <OutlineButton>
                    {this.props.children}
                </OutlineButton>
            </Link>
        )
    }
}


LinkButton.propTypes = {
    to: PropTypes.string.isRequired
}

export default LinkButton;