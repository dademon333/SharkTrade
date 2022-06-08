import {Component} from 'react';
import PropTypes from 'prop-types';

import '../scss/LotCard.scss';
import {Link} from 'react-router-dom';
import TextFunctions from '../../../../TextFunctions';


class LotCard extends Component {
    render = () => {
        const {
            id,
            end_time: endTime,
            max_bid: maxBid,
            is_cancelled: isCancelled,
            item: {name, description, photo_url: photoUrl}
        } = this.props.lot;
        return (
            <Link to={`/lot/${id}`} className="lot-card">
                <div className="lot-card">
                    <img src={photoUrl} alt="img"/>
                    <div className={'lot-card__footer' + (isCancelled ? '' : ' lot-card__footer--separated')}>
                        <div className="lot-card__information">
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
                </div>
            </Link>
        )
    }
}


LotCard.propTypes = {
    lot: PropTypes.object.isRequired,
}

export default LotCard;