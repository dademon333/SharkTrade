import './BidCard.scss';
import TextFunctions from '../../../TextFunctions';


const BidCard = ({bid}) => {
    const {id, amount, created_at: createdAt} = bid;
    let {day, month, hours, minutes} = TextFunctions.parseDateTime(createdAt);

    day = day.toString().padStart(2, '0');
    month = month.toString().padStart(2, '0');
    hours = hours.toString().padStart(2, '0');
    minutes = minutes.toString().padStart(2, '0');

    return (
        <div className="bid-card">
            <div className="bid-card__id"># {id}</div>
            <div className="bid-card__amount">{TextFunctions.reduceNumber(amount)} ₽</div>
            <div className="bid-card__date">
                {`${day}.${month} ${hours}:${minutes}`}
            </div>
        </div>
    )
}

export default BidCard;