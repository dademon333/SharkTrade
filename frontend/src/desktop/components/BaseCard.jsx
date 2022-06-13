import PropTypes from 'prop-types';
import {Component} from 'react';
import {Link} from 'react-router-dom';

import './scss/BaseCard.scss';


class BaseCard extends Component {
    render = () => {
        const {
            link,
            className,
            item: {photo_url: photoUrl},
            children
        } = this.props;

        return (
            <Link to={link} className={`base-card ` + className || ''}>
                <div className={`base-card ` + className || ''}>
                    <img src={photoUrl} alt="img"/>
                    {children}
                </div>
            </Link>
        )
    }
}


BaseCard.propTypes = {
    link: PropTypes.string.isRequired,
    className: PropTypes.string,
    item: PropTypes.object.isRequired
}

export default BaseCard;