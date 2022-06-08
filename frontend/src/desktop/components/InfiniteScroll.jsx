import {Component} from 'react';
import OriginalInfiniteScroll from 'react-infinite-scroller';
import PropTypes from 'prop-types';

import './scss/InfiniteScroll.scss';


class InfiniteScroll extends Component {
    render = () => {
        const {loadMore, hasMore, children} = this.props;

        return (
            <div className="infinite-scroll__wrapper">
                <OriginalInfiniteScroll
                    useWindow={false}
                    loadMore={loadMore}
                    hasMore={hasMore}
                >
                    {children}
                </OriginalInfiniteScroll>
            </div>
        )
    }
}

InfiniteScroll.propTypes = {
    loadMore: PropTypes.func.isRequired,
    hasMore: PropTypes.bool.isRequired
}

export default InfiniteScroll;