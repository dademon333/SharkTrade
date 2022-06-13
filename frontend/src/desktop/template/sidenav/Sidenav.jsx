import {Component} from 'react';

import './Sidenav.scss';
import SidenavButton from './SidenavButton';
import {Icon16SearchOutline, Icon20CubeBoxOutline, Icon16UserOutline} from '@vkontakte/icons';


class Sidenav extends Component {
    render = () => {
        const iconSize = {width: 20, height: 20};

        return (
            <div className="sidenav">
                <SidenavButton
                    to='/explore'
                    text='Лоты'
                    icon={<Icon16SearchOutline {...iconSize}/>}
                />
                <SidenavButton
                    to='/storage'
                    text='Склад'
                    icon={<Icon20CubeBoxOutline {...iconSize}/>}
                />
                <SidenavButton
                    to='/profile'
                    text='Профиль'
                    icon={<Icon16UserOutline {...iconSize}/>}
                />
            </div>
        )
    }
}

export default Sidenav;