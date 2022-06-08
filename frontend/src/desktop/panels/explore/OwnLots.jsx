import {Component} from 'react';
import {connect} from 'react-redux';

import WonderPersikPage from '../../components/WonderPersikPage';
import {ownLotsExtended, ownLotsUpdated} from '../../../slices/Content';
import LoadingSpinnerPage from '../../components/LoadingSpinnerPage';
import PullToRefresh from 'react-simple-pull-to-refresh';
import InfiniteScroll from '../../components/InfiniteScroll';
import LotsContainer from './components/LotsContainer';
import LotCard from './components/LotCard';
import RestAPI from '../../../RestAPI';
import AuthRequiredPage from '../../components/AuthRequiredPage';
import RestAPIErrors from '../../../constants/RestAPIErrors';


class OwnLots extends Component {
    loadLots = async (beforeId) => {
        let {lots, detail} = await RestAPI.getOwnLots(beforeId);

        if (detail === RestAPIErrors.UNAUTHORIZED) {
            return undefined;
        }
        if (detail) {
            lots = []
        }

        if (beforeId) {
            this.props.ownLotsExtended({lots});
        } else {
            this.props.ownLotsUpdated({lots});
        }
    }

    loadMore = async () => {
        const {ownLots} = this.props.content;
        await this.loadLots(ownLots[ownLots.length - 1].id);
    }

    onRefresh = async () => {
        await this.loadLots(null);
    }

    componentDidMount = async () => {
        if (this.props.content.ownLots === null) {
            await this.loadLots(null);
        }
    }

    componentDidUpdate = async () => {
        if (this.props.content.ownLots === null) {
            await this.loadLots(null);
        }
    }

    render = () => {
        const {ownLots, ownLotsLastFetchedAmount} = this.props.content;
        const {id} = this.props.user;

        if (!id) {
            return <AuthRequiredPage />
        }

        if (ownLots === null) {
            return <LoadingSpinnerPage />
        }

        if (ownLots.length === 0) {
            return (
                <PullToRefresh
                    onRefresh={this.onRefresh}
                    pullingContent={null}
                >
                    <WonderPersikPage>
                        Вы еще ничего не продавали
                    </WonderPersikPage>
                </PullToRefresh>
            )
        }

        return (
            <InfiniteScroll
                loadMore={this.loadMore}
                hasMore={ownLotsLastFetchedAmount > 0}
            >
                <PullToRefresh
                    onRefresh={this.onRefresh}
                    pullingContent={null}
                >
                    <LotsContainer>
                        {ownLots.map((x, index) => <LotCard lot={x} key={index} />)}
                    </LotsContainer>
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
    ownLotsUpdated,
    ownLotsExtended
}

export default connect(mapStateToProps, mapDispatchToProps)(OwnLots);