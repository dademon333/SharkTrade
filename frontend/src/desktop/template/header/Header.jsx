import {Component} from 'react';

import './Header.scss';
import {ReactComponent as Logo} from '../../../icons/logo.svg';
import AuthPanel from './AuthPanel';
import {Link} from 'react-router-dom';


class Header extends Component {
    render = () => {
        return (
            <header>
                <div className="content-container--split">
                    <Link to="/" className="logo">
                        <Logo className="logo" />
                    </Link>
                    <div className="header-content">
                        <AuthPanel />
                    </div>
                </div>
            </header>
        )
    }
}

export default Header;