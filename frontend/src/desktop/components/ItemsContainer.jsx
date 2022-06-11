import {Component} from 'react';

import './scss/ItemsContainer.scss';


class ItemsContainer extends Component {
    render() {
        return (
            <div className="items-container">
                {this.props.children}
            </div>
        )
    }
}


export default ItemsContainer;