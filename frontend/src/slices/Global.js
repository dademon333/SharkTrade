import {createSlice} from '@reduxjs/toolkit';

const globalSlice = createSlice({
    name: 'global',
    initialState: {
        accessToken: undefined,
        isMobile: false,
        online: 0,

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
        onlineChanged(state, action) {
            state.online = action.payload;
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
    onlineChanged,

    screenSpinnerChanged,
    modalChanged
} = globalSlice.actions;