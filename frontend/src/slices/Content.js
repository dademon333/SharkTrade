import {createSlice} from '@reduxjs/toolkit';

const contentSlice = createSlice({
    name: 'content',
    initialState: {
        allLots: null,
        allLotsLastFetchedAmount: null,

        ownLots: null,
        ownLotsLastFetchedAmount: null
    },
    reducers: {
        allLotsUpdated(state, action) {
            const {lots} = action.payload;
            state.allLots = lots;
            state.allLotsLastFetchedAmount = lots.length;
        },
        allLotsExtended(state, action) {
            const {lots} = action.payload;
            state.allLots = (state.allLots || []).concat(lots);
            state.allLotsLastFetchedAmount = lots.length;
        },

        ownLotsUpdated(state, action) {
            if (action.payload) {
                const {lots} = action.payload;
                state.ownLots = lots;
                state.ownLotsLastFetchedAmount = lots.length;
            } else {
                state.ownLots = null;
                state.ownLotsLastFetchedAmount = null;
            }
        },
        ownLotsExtended(state, action) {
            const {lots} = action.payload;
            state.ownLots = (state.ownLots || []).concat(lots);
            state.ownLotsLastFetchedAmount = lots.length;
        }
    }
});

export default contentSlice.reducer;
export const {
    allLotsUpdated,
    allLotsExtended,
    ownLotsUpdated,
    ownLotsExtended
} = contentSlice.actions;