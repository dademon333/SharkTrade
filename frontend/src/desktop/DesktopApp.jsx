import {Component} from 'react';
import {Routes, Route, BrowserRouter as Router} from 'react-router-dom';

import IndexPage from './pages/index/IndexPage';
import Page404 from './pages/page404/Page404';
import Explore from './pages/explore/Explore';
import Storage from './pages/storage/Storage';
import Profile from './pages/profile/Profile';
import LotPage from './pages/lot/LotPage';
import ItemPage from './pages/item/ItemPage';


class DesktopApp extends Component {
    render = () => {
        return (
            <Router>
                <Routes>
                    <Route path="/" element={<IndexPage />}/>
                    <Route path="/explore" element={<Explore />}/>
                    <Route path="/storage" element={<Storage />}/>
                    <Route path="/profile" element={<Profile />}/>
                    <Route path="/lot/:id" element={<LotPage />}/>
                    <Route path="/item/:id" element={<ItemPage />}/>
                    <Route path="*" element={<Page404 />}/>
                </Routes>
            </Router>
        )
    }
}

export default DesktopApp;