import {Component} from 'react';
import {connect} from 'react-redux';
import {Routes, Route, BrowserRouter as Router} from 'react-router-dom';

import IndexPage from './pages/index/IndexPage';
import Page404 from './pages/page404/Page404';
import Explore from './pages/explore/Explore';
import Inventory from './pages/indentory/Inventory';
import Profile from './pages/profile/Profile';
import LotPage from './pages/Lot/LotPage';


class DesktopApp extends Component {
    render = () => {
        return (
            <Router>
                <Routes>
                    <Route path="/" element={<IndexPage />}/>
                    <Route path="/explore" element={<Explore />}/>
                    <Route path="/inventory" element={<Inventory />}/>
                    <Route path="/profile" element={<Profile />}/>
                    <Route path="/lot/:id" element={<LotPage />}/>
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