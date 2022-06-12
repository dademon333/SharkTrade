import {Component} from 'react';
import persik from '../img/persik_wonder__clown.png';

import './MobileApp.scss';


class MobileApp extends Component {
    render = () => {
        return (
            <main>
                <img src={persik} alt="persik" className="persik"/>
                <div className="caption">Мобильная версия в разработке, заходите с компутера</div>
            </main>
        )
    }
}

export default MobileApp;