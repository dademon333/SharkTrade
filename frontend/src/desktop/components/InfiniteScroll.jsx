import {Component} from 'react';
import PullToRefresh from 'react-simple-pull-to-refresh';
import OriginalInfiniteScroll from 'react-infinite-scroller';

import './scss/InfiniteScroll.scss';
import PropTypes from 'prop-types';


class InfiniteScroll extends Component {
    render = () => {
        const {children, loadMore, hasMore, onRefresh} = this.props;

        return (
            <OriginalInfiniteScroll
                loadMore={loadMore}
                hasMore={hasMore}
                className="infinite-scroll"
            >
                <PullToRefresh
                    onRefresh={onRefresh}
                    pullingContent={null}
                >
                    {children}
                </PullToRefresh>
            </OriginalInfiniteScroll>
        )
    }
}


InfiniteScroll.propTypes = {
    loadMore: PropTypes.func.isRequired,
    hasMore: PropTypes.bool.isRequired,
    onRefresh: PropTypes.func.isRequired
}

export default InfiniteScroll;