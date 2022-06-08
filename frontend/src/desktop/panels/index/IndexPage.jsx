import {Component} from 'react';

import Template from '../../template/Template';
import persik from '../../../img/persik_shy.png';

import './IndexPage.scss';
import LinkButton from '../../components/LinkButton';


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
                    <LinkButton to="/explore">Погнали</LinkButton>
                </div>
            </Template>
        )
    }
}

export default IndexPage;