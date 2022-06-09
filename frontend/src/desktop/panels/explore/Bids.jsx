import PullToRefresh from 'react-simple-pull-to-refresh';
import {Component} from 'react';
import {connect} from 'react-redux';

import WonderPersikPage from '../../components/WonderPersikPage';
import AuthRequiredPage from '../../components/AuthRequiredPage';
import LoadingSpinnerPage from '../../components/LoadingSpinnerPage';
import InfiniteScroll from '../../components/InfiniteScroll';
import ItemsContainer from '../../components/ItemsContainer';
import {ownBidsExtended, ownBidsUpdated} from '../../../slices/Content';
import BidCard from './components/BidCard';
import RestAPI from '../../../RestAPI';
import RestAPIErrors from '../../../constants/RestAPIErrors';


class Bids extends Component {
    loadBids = async (beforeId) => {
        let {bids, detail} = await RestAPI.getOwnBids(beforeId);

        if (detail === RestAPIErrors.UNAUTHORIZED) {
            return;
        }
        if (detail) {
            bids = []
        }

        if (beforeId) {
            this.props.ownBidsExtended({bids});
        } else {
            this.props.ownBidsUpdated({bids});
        }
    }

    loadMore = async () => {
        const {ownBids} = this.props.content;
        await this.loadBids(ownBids[ownBids.length - 1].id);
    }

    onRefresh = async () => {
        await this.loadBids(null);
    }

    componentDidMount = async () => {
        if (this.props.content.ownBids === null) {
            await this.loadBids(null);
        }
    }

    componentDidUpdate = async () => {
        if (this.props.content.ownBids === null) {
            await this.loadBids(null);
        }
    }

    render = () => {
        const {ownBids, ownBidsLastFetchedAmount} = this.props.content;
        const {id} = this.props.user;

        if (!id) {
            return <AuthRequiredPage />
        }

        if (ownBids === null) {
            return <LoadingSpinnerPage />
        }

        if (ownBids.length === 0) {
            return (
                <PullToRefresh
                    onRefresh={this.onRefresh}
                    pullingContent={null}
                >
                    <WonderPersikPage>
                        Вы еще не делали ставки
                    </WonderPersikPage>
                </PullToRefresh>
            )
        }

        return (
            <InfiniteScroll
                loadMore={this.loadMore}
                hasMore={ownBidsLastFetchedAmount > 0}
            >
                <PullToRefresh
                    onRefresh={this.onRefresh}
                    pullingContent={null}
                >
                    <ItemsContainer>
                        {ownBids.map((x, index) => <BidCard bid={x} key={index} />)}
                    </ItemsContainer>
                </PullToRefresh>
            </InfiniteScroll>
        )
    }
}


const mapStateToProps = (state) => ({
    user: state.user,
    content: state.content
})

const mapDispatchToProps = {
    ownBidsUpdated,
    ownBidsExtended
}

export default connect(mapStateToProps, mapDispatchToProps)(Bids);