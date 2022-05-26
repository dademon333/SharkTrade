import {Component} from 'react';
import {connect} from 'react-redux';

import MobileApp from './mobile/MobileApp';
import DesktopApp from './desktop/DesktopApp';


class App extends Component {
    render = () => {
        if (this.props.global.isMobile)
            return <MobileApp />
        else
            return <DesktopApp />
    }
}


const mapStateToProps = (state) => {
    return {
        global: state.global
    }
}

const mapDispatchToProps = {

}

export default connect(mapStateToProps, mapDispatchToProps)(App);