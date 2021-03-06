import React from 'react';
import ReactDOM from 'react-dom/client';
import {Provider} from 'react-redux';

import App from './App';
import {store} from './Store';
import matchMedia from './MatchMedia';
import './index.scss';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <Provider store={store}>
        <App/>
    </Provider>
);

matchMedia();
window.addEventListener('resize', matchMedia);