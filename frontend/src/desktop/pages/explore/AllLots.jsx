import {Component} from 'react';
import {connect} from 'react-redux';

import LoadingSpinnerPage from '../../components/LoadingSpinnerPage';
import WonderPersikPage from '../../components/WonderPersikPage';
import RestAPI from '../../../RestAPI';
import {allLotsExtended, allLotsUpdated} from '../../../slices/Content';
import LotCard from './components/LotCard';
import ItemsContainer from '../../components/ItemsContainer';
import InfiniteScroll from '../../components/InfiniteScroll';


class AllLots extends Component {
    loadLots = async (beforeId) => {
        let {lots, detail} = await RestAPI.getAllLots(beforeId);
        if (detail) {
            lots = []
        }
        if (beforeId) {
            this.props.allLotsExtended({lots});
        } else {
            this.props.allLotsUpdated({lots});
        }
    }

    loadMore = async () => {
        const {allLots} = this.props.content;
        await this.loadLots(allLots[allLots.length - 1].id);
    }

    onRefresh = async () => {
        await this.loadLots(null);
    }

    componentDidMount = async () => {
        if (this.props.content.allLots === null) {
            await this.loadLots(null);
        }
    }

    componentDidUpdate = async () => {
        if (this.props.content.allLots === null) {
            await this.loadLots(null);
        }
    }

    withInfiniteScroll = (content) => {
        const {allLotsLastFetchedAmount} = this.props.content;
        return (
            <InfiniteScroll
                loadMore={this.loadMore}
                hasMore={allLotsLastFetchedAmount > 0}
                onRefresh={this.onRefresh}
            >
                {content}
            </InfiniteScroll>
        )
    }

    render = () => {
        const {allLots} = this.props.content;

        if (allLots === null) {
            return this.withInfiniteScroll(<LoadingSpinnerPage />);
        }

        if (allLots.length === 0) {
            return this.withInfiniteScroll(<WonderPersikPage>Сейчас нет активных лотов</WonderPersikPage>);
        }

        return this.withInfiniteScroll(
            <ItemsContainer>
                {allLots.map((x, index) => <LotCard lot={x} key={index} />)}
            </ItemsContainer>
        );
    }
}


const mapStateToProps = (state) => ({
    content: state.content
})

const mapDispatchToProps = {
    allLotsUpdated,
    allLotsExtended
}

export default connect(mapStateToProps, mapDispatchToProps)(AllLots);