import {Component} from 'react';
import {connect} from 'react-redux';
import {Routes, Route, BrowserRouter as Router} from 'react-router-dom';

import IndexPage from './panels/index/IndexPage';
import Page404 from './panels/page404/Page404';
import Explore from './panels/explore/Explore';
import Inventory from './panels/indentory/Inventory';
import Profile from './panels/profile/Profile';


class DesktopApp extends Component {
    render = () => {
        return (
            <Router>
                <Routes>
                    <Route path="/" element={<IndexPage />}/>
                    <Route path="/explore" element={<Explore />}/>
                    <Route path="/inventory" element={<Inventory />}/>
                    <Route path="/profile" element={<Profile />}/>
                    <Route path="*" element={<Page404 />}/>
                </Routes>
            </Router>
        )
    }
}


const mapStateToProps = (state) => ({
})

const mapDispatchToProps = {

}

export default connect(mapStateToProps, mapDispatchToProps)(DesktopApp);