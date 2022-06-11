import {Component} from 'react';
import {CircularProgress} from '@mui/material';

import './scss/LoadingSpinnerPage.scss';


class LoadingSpinnerPage extends Component {
    render = () => {
        return (
            <div className="loading-spinner-page">
                <CircularProgress color="inherit" size={80} />
            </div>
        )
    }
}


export default LoadingSpinnerPage;