import {Component} from 'react';

import './Header.scss';
import {ReactComponent as Logo} from '../../../icons/logo.svg';
import AuthPanel from './AuthPanel';


class Header extends Component {
    render = () => {
        return (
            <header>
                <div className="content-container--split">
                    <Logo className="logo" />
                    <div className="header-content">
                        <AuthPanel />
                    </div>
                </div>
            </header>
        )
    }
}

export default Header;