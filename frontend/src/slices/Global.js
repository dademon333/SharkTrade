import {createSlice} from '@reduxjs/toolkit';

const globalSlice = createSlice({
    name: 'global',
    initialState: {
        isMobile: false
    },
    reducers: {
        isMobileChanged(state, action) {
            state.isMobile = action.payload;
        }
    }
});

export default globalSlice.reducer;
export const {
    isMobileChanged
} = globalSlice.actions;