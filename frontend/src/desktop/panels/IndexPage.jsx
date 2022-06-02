import {Component} from 'react';
import {Link} from 'react-router-dom';

import Template from '../template/Template';
import persik from '../../img/persik_shy.png';

import './scss/IndexPage.scss';


class IndexPage extends Component {
    render = () => {
        return (
            <Template className="index-page">
                <img src={persik} alt="persik" className="persik"/>
                <div className="about">
                    <div className="about__header">
                        Исследуйте, собирайте и продавайте необычные товары
                    </div>
                    <div className="about__caption">
                        Shark Trade - первая и крупнейшая в мире торговая площадка
                    </div>
                    <Link to="/explore" className="link-button">
                        Погнали
                    </Link>
                </div>
            </Template>
        )
    }
}

export default IndexPage;