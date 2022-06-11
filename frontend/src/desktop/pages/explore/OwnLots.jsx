import {Component} from 'react';
import {connect} from 'react-redux';

import WonderPersikPage from '../../components/WonderPersikPage';
import {ownLotsExtended, ownLotsUpdated} from '../../../slices/Content';
import LoadingSpinnerPage from '../../components/LoadingSpinnerPage';
import ItemsContainer from '../../components/ItemsContainer';
import LotCard from './components/LotCard';
import RestAPI from '../../../RestAPI';
import AuthRequiredPage from '../../components/AuthRequiredPage';
import RestAPIErrors from '../../../constants/RestAPIErrors';
import InfiniteScroll from '../../components/InfiniteScroll';


class OwnLots extends Component {
    loadLots = async (beforeId) => {
        let {lots, detail} = await RestAPI.getOwnLots(beforeId);

        if (detail === RestAPIErrors.UNAUTHORIZED) {
            return;
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

    withInfiniteScroll = (content) => {
        const {ownLotsLastFetchedAmount} = this.props.content;
        return (
            <InfiniteScroll
                loadMore={this.loadMore}
                hasMore={ownLotsLastFetchedAmount > 0}
                onRefresh={this.onRefresh}
            >
                {content}
            </InfiniteScroll>
        )
    }

    render = () => {
        const {ownLots} = this.props.content;
        const {id} = this.props.user;

        if (!id) {
            return this.withInfiniteScroll(<AuthRequiredPage />);
        }

        if (ownLots === null) {
            return this.withInfiniteScroll(<LoadingSpinnerPage />);
        }

        if (ownLots.length === 0) {
            return this.withInfiniteScroll(<WonderPersikPage>Вы еще ничего не продавали</WonderPersikPage>);
        }

        return this.withInfiniteScroll(
            <ItemsContainer>
                {ownLots.map((x, index) => <LotCard lot={x} key={index} />)}
            </ItemsContainer>
        );
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