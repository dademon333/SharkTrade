import {createSlice} from '@reduxjs/toolkit';

const globalSlice = createSlice({
    name: 'global',
    initialState: {
        accessToken: null,
        isMobile: false,
        online: 0,

        screenSpinner: false,
        modal: null,

        alertVariant: null,
        alertSeverity: null,
        alertText: null
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
        },

        alertChanged(state, action) {
            if (action.payload) {
                state.alertVariant = action.payload.alertVariant;
                state.alertSeverity = action.payload.alertSeverity;
                state.alertText = action.payload.alertText;
            } else {
                state.alertVariant = null;
                state.alertSeverity = null;
                state.alertText = null;
            }
        }
    }
});

export default globalSlice.reducer;
export const {
    accessTokenChanged,
    isMobileChanged,
    onlineChanged,

    screenSpinnerChanged,
    modalChanged,

    alertChanged
} = globalSlice.actions;