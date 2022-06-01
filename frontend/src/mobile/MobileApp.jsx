import {Component} from 'react';
import {connect} from 'react-redux';


class MobileApp extends Component {
    render = () => {
        return (
            <div>Mobile app</div>
        )
    }
}


const mapStateToProps = (state) => ({
})

const mapDispatchToProps = {

}

export default connect(mapStateToProps, mapDispatchToProps)(MobileApp);