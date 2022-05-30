import {createSlice} from '@reduxjs/toolkit';

const globalSlice = createSlice({
    name: 'global',
    initialState: {
        accessToken: undefined,
        isMobile: false,

        screenSpinner: false,
        modal: null
    },
    reducers: {
        accessTokenChanged(state, action) {
            state.accessToken = action.payload;
        },
        isMobileChanged(state, action) {
            state.isMobile = action.payload;
        },

        screenSpinnerChanged(state, action) {
            state.screenSpinner = action.payload;
        },
        modalChanged(state, action) {
            state.modal = action.payload;
        }
    }
});

export default globalSlice.reducer;
export const {
    accessTokenChanged,
    isMobileChanged,
    screenSpinnerChanged,
    modalChanged
} = globalSlice.actions;