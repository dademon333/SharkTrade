import {Component} from 'react';

import Template from '../../template/Template';
import persik from '../../../img/persik_resent__scaled.png';

import './Panel404.scss';
import LinkButton from '../../components/LinkButton';


class Page404 extends Component {
    render = () => {
        return (
            <Template className="page-404">
                <img src={persik} alt="persik" className="persik"/>
                <div className="caption">Здесь ничего нет</div>
                <LinkButton to="/">Домой</LinkButton>
            </Template>
        )
    }
}

export default Page404;