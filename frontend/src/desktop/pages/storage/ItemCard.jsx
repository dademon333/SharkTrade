import {Component} from 'react';
import PropTypes from 'prop-types';

import BaseCard from '../../components/BaseCard';

import './ItemCard.scss';


class ItemCard extends Component {
    render = () => {
        const {
            item,
            item: {id, name, description},
        } = this.props;

        return (
            <BaseCard item={item} link={`/item/${id}`} className="item-card">
                <div className="item-card__footer">
                    <div className="item-card__name truncatable">
                        {name}
                    </div>
                    <div className="item-card__description">
                        {description}
                    </div>
                </div>
            </BaseCard>
        )
    }
}


ItemCard.propTypes = {
    item: PropTypes.object.isRequired
}

export default ItemCard;