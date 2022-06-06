import {Component} from 'react';
import {NavLink} from 'react-router-dom';
import PropTypes from 'prop-types';

class SidenavButton extends Component {
    render = () => {
        const {to, text, icon} = this.props;
        return (
            <NavLink
                to={to}
                className={({isActive}) => "sidenav__button" + (isActive ? " sidenav__button--active" : "")}
            >
                {icon}
                {text}
            </NavLink>
        )
    }
}


SidenavButton.propTypes = {
    to: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired
}

export default SidenavButton;