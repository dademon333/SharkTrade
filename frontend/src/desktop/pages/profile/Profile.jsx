import {Component} from 'react';

import Template from '../../template/Template';
import WonderPersikPage from '../../components/WonderPersikPage';

import './Profile.scss';


class Profile extends Component {
    render = () => {
        return (
            <Template navigation={true} className="profile">
                <WonderPersikPage>
                    Раздел в разработке
                </WonderPersikPage>
            </Template>
        )
    }
}

export default Profile;