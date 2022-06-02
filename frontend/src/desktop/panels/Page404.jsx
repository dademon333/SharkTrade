import {Component} from 'react';

import Template from '../template/Template';
import persik from '../../icons/persik_woner.png';

import './scss/Panel404.scss';
import {Link} from 'react-router-dom';


class Page404 extends Component {
    render = () => {
        return (
            <Template className="page-404">
                <img src={persik} alt="persik" className="persik"/>
                <div className="caption">тут ничего нет...</div>
                <Link to="/" className="link-button">Домой</Link>
            </Template>
        )
    }
}

export default Page404;