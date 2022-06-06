import {Component} from 'react';

import Template from '../template/Template';
import WonderPersikPage from '../components/WonderPersikPage';


class Explore extends Component {
    state = {
        page: 1,
        lots: []
    }

    componentDidMount() {

    }

    render = () => {
        console.log(this.state.lots);

        if (this.state.lots.length === 0) {
            return (
                <Template navigation={true}>
                    <WonderPersikPage>
                        Сейчас нет активных лотов
                    </WonderPersikPage>
                </Template>
            )
        }
        return (
            <Template navigation={true}>
                test
            </Template>
        )
    }
}

export default Explore;