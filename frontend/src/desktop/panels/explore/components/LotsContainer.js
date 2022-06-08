import {Component} from 'react';


class LotsContainer extends Component {
    render() {
        return (
            <div className="lots-container">
                {this.props.children}
            </div>
        )
    }
}


export default LotsContainer;