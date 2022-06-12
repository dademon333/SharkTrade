import {useParams} from 'react-router-dom';
import {useEffect} from 'react';
import {connect} from 'react-redux';

import Template from '../../template/Template';
import Page404 from '../page404/Page404';
import TextFunctions from '../../../TextFunctions';
import RestAPI from '../../../RestAPI';
import LoadingSpinnerPage from '../../components/LoadingSpinnerPage';
import BidCard from './BidCard';
import OutlineButton from '../../components/OutlineButton';
import {ReactComponent as Article} from '../../../icons/article.svg';
import {ReactComponent as Clock} from '../../../icons/clock.svg';
import {ReactComponent as Billhead} from '../../../icons/billhead.svg';
import {modalChanged} from '../../../slices/Global';
import Modals from '../../../constants/Modals';
import {lotPageLotDataChanged} from '../../../slices/Content';

import './LotPage.scss';
import LinkButton from '../../components/LinkButton';


const withTemplate = (content) => (
    <Template className={'lot-page'}>
        {content}
    </Template>
)


const LotPage = (props) => {
    let {id: lotId} = useParams();
    lotId = parseInt(lotId);

    const {lotPageLotDataChanged} = props;
    const lot = props.content.lotPageLotsData[lotId];

    useEffect(() => {
        const getLot = async () => {
            const lot = await RestAPI.getLot(lotId);
            lotPageLotDataChanged({lotId, lot});
        }

        if (lot === undefined && TextFunctions.isNatural(lotId)) {
            getLot().then();
        }
    });

    if (!TextFunctions.isNatural(lotId)) {
        return <Page404/>
    }

    if (lot === undefined) {
        return withTemplate(<LoadingSpinnerPage />)
    }

    if (lot.detail) {
        return <Page404/>
    }

    let {
        bids,
        is_cancelled: isCancelled,
        max_bid: maxBid,
        end_time: endTime,
        owner_id: ownerId,
        item: {
            name,
            description,
            photo_url: photoUrl
        }
    } = lot;
    bids = [...bids].reverse().slice(0, 3);

    return withTemplate(
        <>
            <div className="left-part">
                <img src={photoUrl} alt="фото" />
                <div className="description frame">
                    <div className="description__header">
                        <Article />
                        Описание
                    </div>
                    <div className="description__text">
                        {description}
                    </div>
                </div>
                <LinkButton to="/explore">Назад к лотам</LinkButton>
            </div>
            <div className="right-part">
                <div className="name">{name}</div>
                <div className="sale-frame frame">
                    <div className="sale-frame__end-time">
                        <Clock/>
                        До {TextFunctions.formatDateTime(endTime)}
                    </div>
                    <div className="max-bid">
                        <div>
                            Максимальная ставка:
                            <div className="max-bid__amount">{TextFunctions.formatNumber(maxBid)} ₽</div>
                        </div>
                        <div>
                            {!isCancelled
                                && props.user.id !== ownerId
                                && (
                                    <OutlineButton
                                        onClick={() => props.modalChanged(Modals.CREATE_BID)}
                                    >
                                        Повысить
                                    </OutlineButton>
                                )
                            }
                        </div>
                    </div>
                </div>
                <div className="bids frame">
                    <div className="bids__header">
                        <Billhead />
                        Ставки
                    </div>
                    <div className="bids__content">
                        {bids.map((x, index) => <BidCard bid={x} key={index}/>)}
                    </div>
                </div>
            </div>
        </>
    );
}


const mapStateToProps = (state) => ({
    user: state.user,
    content: state.content
});

const mapDispatchToProps = {
    modalChanged,
    lotPageLotDataChanged
}

export default connect(mapStateToProps, mapDispatchToProps)(LotPage);