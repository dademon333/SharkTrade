import {Component} from 'react';
import {connect} from 'react-redux';

import Template from './template/Template';


class DesktopApp extends Component {
    render = () => {
        return (
            <Template>
                <div>While using the issue tracker ID itself is sufficient to identify a unique branch in a project in most cases, there could be chances that some more nuance is needed. For example, there could be multiple branches needed to work on one issue, possibly by different people</div>
            </Template>
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