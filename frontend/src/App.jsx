import {Component} from 'react';
import {connect} from 'react-redux';

import MobileApp from './mobile/MobileApp';
import DesktopApp from './desktop/DesktopApp';
import {screenSpinnerChanged} from './slices/Global';

import 'rsuite/dist/rsuite.min.css';
import SystemFunctions from './SystemFunctions';


class App extends Component {
    componentDidMount = async () => {
        this.props.screenSpinnerChanged(true);
        await SystemFunctions.connectBackend();
        this.props.screenSpinnerChanged(false);
    }

    render = () => {
        if (this.props.global.isMobile)
            return <MobileApp />
        else
            return <DesktopApp />
    }
}


const mapStateToProps = (state) => ({
    global: state.global,
    user: state.user
})

const mapDispatchToProps = {
    screenSpinnerChanged,
}

export default connect(mapStateToProps, mapDispatchToProps)(App);