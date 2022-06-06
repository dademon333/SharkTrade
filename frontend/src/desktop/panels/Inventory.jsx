import {Component} from 'react';

import Template from '../template/Template';
import WonderPersikPage from '../components/WonderPersikPage';


class Inventory extends Component {
    render = () => {
        return (
            <Template navigation={true}>
                <WonderPersikPage>
                    Раздел в разработке
                </WonderPersikPage>
            </Template>
        )
    }
}

export default Inventory;