import {createSlice} from '@reduxjs/toolkit';

const contentSlice = createSlice({
    name: 'content',
    initialState: {
        allLots: null,
        allLotsLastFetchedAmount: null
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
        }
    }
});

export default contentSlice.reducer;
export const {
    allLotsUpdated,
    allLotsExtended
} = contentSlice.actions;