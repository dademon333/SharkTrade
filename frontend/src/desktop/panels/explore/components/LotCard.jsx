import {Component} from 'react';
import PropTypes from 'prop-types';

import '../scss/LotCard.scss';
import TextFunctions from '../../../../TextFunctions';
import ItemCard from '../../../components/ItemCard';


class LotCard extends Component {
    render = () => {
        const {
            id,
            end_time: endTime,
            max_bid: maxBid,
            is_cancelled: isCancelled,
            item,
            item: {name, description}
        } = this.props.lot;
        return (
            <ItemCard item={item} link={`/lot/${id}`} className="lot-card">
                 <div className={'lot-card__footer' + (isCancelled ? '' : ' lot-card__footer--separated')}>
                     <div className="lot-card__item-information">
                         <div className="lot-card__name truncatable">
                             {name}
                         </div>
                         <div className="lot-card__description">
                             {description}
                         </div>
                     </div>
                     {!isCancelled && (
                         <div className="lot-card__pricing">
                             <div className="lot-card__price">
                                 {TextFunctions.reduceNumber(maxBid)}
                             </div>
                             <div className="lot-card__remaining">
                                 {TextFunctions.getRemainingTime(endTime)}
                             </div>
                         </div>
                     )}
                 </div>
            </ItemCard>
        )
    }
}


LotCard.propTypes = {
    lot: PropTypes.object.isRequired,
}

export default LotCard;