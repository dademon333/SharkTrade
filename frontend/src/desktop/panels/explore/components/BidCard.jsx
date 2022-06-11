import {Component} from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';


import RestAPI from '../../../../RestAPI';
import ItemCard from '../../../components/ItemCard';
import TextFunctions from '../../../../TextFunctions';
import OutlineButton from '../../../components/OutlineButton';
import {alertChanged} from '../../../../slices/Global';
import {balanceChanged} from '../../../../slices/User';
import {bidWithdrawn} from '../../../../slices/Content';
import RestAPIErrors from '../../../../constants/RestAPIErrors';
import AlertVariant from '../../../../constants/AlertVariant';
import AlertSeverity from '../../../../constants/AlertSeverity';
import {ReactComponent as Check} from '../../../../icons/check.svg';
import {ReactComponent as Cancel} from '../../../../icons/cancel.svg';
import {ReactComponent as Clock} from '../../../../icons/clock.svg';

import '../scss/BidCard.scss';


class BidCard extends Component {
    onWithdraw = async (bidId, amount) => {
        const {new_balance: newBalance, detail} = await RestAPI.withdrawBid(bidId);
        if (detail) {
            this.props.alertChanged({
                alertVariant: AlertVariant.OUTLINED,
                alertSeverity: AlertSeverity.ERROR,
                alertText: RestAPIErrors.TRANSLATIONS[detail]
            })
            this.props.bidWithdrawn(bidId);
            return;
        }

        this.props.balanceChanged(newBalance);
        this.props.bidWithdrawn(bidId);
        this.props.alertChanged({
            alertVariant: AlertVariant.OUTLINED,
            alertSeverity: AlertSeverity.SUCCESS,
            alertText: `+ ${TextFunctions.formatNumber(amount)} ₽`
        })
    }

    getIcon = (status) => {
        switch (status) {
            case 'win':
                return <Check className="bid-card__result bid-card__result--win"/>;
            case 'highest':
                return <Clock className="bid-card__result bid-card__result--highest"/>;
            case 'lose':
                return <Cancel className="bid-card__result bid-card__result--lose"/>
            default:
                console.log('Unknown bid status: ', status);
        }
    }

    render = () => {
        const {
            id: bidId,
            amount,
            lot_id: lotId,
            can_withdraw: canWithdraw,
            status,
            item,
            item: {name}
        } = this.props.bid;

        return (
            <div className="bid-card__wrapper">
                <ItemCard item={item} link={`/lot/${lotId}`} className="bid-card">
                    <div className="bid-card__footer">
                        <div className="bid-card__item-information">
                            <div className="bid-card__name truncatable">{name}</div>
                        </div>
                        <div className="bid-card__rate-information">
                            <div className="bid-card__rate">{TextFunctions.reduceNumber(amount)}</div>
                            {this.getIcon(status)}
                        </div>
                    </div>
                </ItemCard>
                {canWithdraw && (
                    <OutlineButton
                        onClick={async () => await this.onWithdraw(bidId, amount)}
                    >
                        Вернуть ₽
                    </OutlineButton>
                )}
            </div>
        )
    }
}


BidCard.propTypes = {
    bid: PropTypes.object.isRequired
}

const mapDispatchToProps = {
    alertChanged,
    balanceChanged,
    bidWithdrawn
}

export default connect(null, mapDispatchToProps)(BidCard);