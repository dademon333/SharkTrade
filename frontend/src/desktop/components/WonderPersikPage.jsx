import {Component} from 'react';

import './scss/WonderPersikPage.scss';
import persik from '../../img/persik_wonder__scaled.png';


class WonderPersikPage extends Component {
    render = () => {
        return (
            <div className="wonder-persik-page">
                <img src={persik} alt="persik"/>
                {this.props.children}
            </div>
        )
    }
}


export default WonderPersikPage;