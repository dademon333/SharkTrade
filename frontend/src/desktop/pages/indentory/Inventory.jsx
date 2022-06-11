import {Component} from 'react';
import {connect} from 'react-redux';

import Template from '../../template/Template';
import WonderPersikPage from '../../components/WonderPersikPage';
import {ownItemsExtended, ownItemsUpdated} from '../../../slices/Content';
import AuthRequiredPage from '../../components/AuthRequiredPage';
import LoadingSpinnerPage from '../../components/LoadingSpinnerPage';
import ItemsContainer from '../../components/ItemsContainer';
import RestAPI from '../../../RestAPI';
import RestAPIErrors from '../../../constants/RestAPIErrors';
import InfiniteScroll from '../../components/InfiniteScroll';
import ItemCard from './ItemCard';


class Inventory extends Component {
    loadItems = async (beforeId) => {
        let {items, detail} = await RestAPI.getOwnItems(beforeId);

        if (detail === RestAPIErrors.UNAUTHORIZED) {
            return;
        }
        if (detail) {
            items = []
        }

        if (beforeId) {
            this.props.ownItemsExtended({items});
        } else {
            this.props.ownItemsUpdated({items});
        }
    }

    loadMore = async () => {
        const {ownItems} = this.props.content;
        await this.loadItems(ownItems[ownItems.length - 1].id);
    }

    onRefresh = async () => {
        await this.loadItems(null);
    }

    componentDidMount = async () => {
        if (this.props.content.ownItems === null) {
            await this.loadItems(null);
        }
    }

    componentDidUpdate = async () => {
        if (this.props.content.ownItems === null) {
            await this.loadItems(null);
        }
    }

    withTemplate = (content) => {
        const {ownItemsLastFetchedAmount} = this.props.content;
        return (
            <Template navigation={true} className="inventory">
                <InfiniteScroll
                    loadMore={this.loadMore}
                    hasMore={ownItemsLastFetchedAmount > 0}
                    onRefresh={this.onRefresh}
                >
                    {content}
                </InfiniteScroll>
            </Template>
        )
    }

    render = () => {
        const {ownItems} = this.props.content;
        const {id} = this.props.user;

        if (!id) {
            return this.withTemplate(<AuthRequiredPage />);
        }

        if (ownItems === null) {
            return this.withTemplate(<LoadingSpinnerPage />);
        }

        if (ownItems.length === 0) {
            return this.withTemplate(<WonderPersikPage>На Вашем складе пусто</WonderPersikPage>);
        }

        return this.withTemplate(
            <ItemsContainer>
                {ownItems.map((x, index) =>
                    <ItemCard item={x} key={index}/>
                )}
            </ItemsContainer>
        )
    }
}

const mapStateToProps = (state) => ({
    user: state.user,
    content: state.content
})

const mapDispatchToProps = {
    ownItemsUpdated,
    ownItemsExtended
}

export default connect(mapStateToProps, mapDispatchToProps)(Inventory);