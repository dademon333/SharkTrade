import PropTypes from 'prop-types';
import {Component} from 'react';
import {Link} from 'react-router-dom';

import './scss/ItemCard.scss';


class ItemCard extends Component {
    render = () => {
        const {
            link,
            className,
            item: {photo_url: photoUrl},
            children
        } = this.props;

        return (
            <Link to={link} className={`item-card ${className}`}>
                <div className={`item-card ${className}`}>
                    <img src={photoUrl} alt="img"/>
                    {children}
                </div>
            </Link>
        )
    }
}


ItemCard.propTypes = {
    link: PropTypes.string,
    className: PropTypes.string,
    item: PropTypes.object.isRequired
}

export default ItemCard;