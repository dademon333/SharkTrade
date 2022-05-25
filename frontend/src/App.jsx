import {Component} from 'react';
import {connect} from 'react-redux';

class App extends Component {
    render = () => {
        return (
            <div>test div</div>
        )
    }
}


const mapStateToProps = (state) => {
    return {

    }
}

const mapDispatchToProps = {

}

export default connect(mapStateToProps, mapDispatchToProps)(App);