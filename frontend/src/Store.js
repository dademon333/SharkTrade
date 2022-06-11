import {configureStore} from '@reduxjs/toolkit';

import globalSlice from './slices/Global';
import userSlice from './slices/User';
import contentSlice from './slices/Content';


export const store = configureStore({
    reducer: {
        global: globalSlice,
        user: userSlice,
        content: contentSlice
    }
})