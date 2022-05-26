import {Component} from 'react';
import {connect} from 'react-redux';


class DesktopApp extends Component {
    render = () => {
        return (
            <div>Desktop app</div>
        )
    }
}


const mapStateToProps = (state) => {
    return {

    }
}

const mapDispatchToProps = {

}

export default connect(mapStateToProps, mapDispatchToProps)(DesktopApp);