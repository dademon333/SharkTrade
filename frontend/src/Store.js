import {configureStore} from '@reduxjs/toolkit';

import globalSlice from './slices/Global';


export const store = configureStore({
    reducer: {
        global: globalSlice
    }
})