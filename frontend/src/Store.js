import {configureStore} from '@reduxjs/toolkit';

import globalSlice from './slices/Global';
import userSlice from './slices/User';


export const store = configureStore({
    reducer: {
        global: globalSlice,
        user: userSlice
    }
})