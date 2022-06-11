import {createSlice} from '@reduxjs/toolkit';

const contentSlice = createSlice({
    name: 'content',
    initialState: {
        allLots: null,
        allLotsLastFetchedAmount: null,

        ownLots: null,
        ownLotsLastFetchedAmount: null,

        ownBids: null,
        ownBidsLastFetchedAmount: null
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
        },

        ownBidsUpdated(state, action) {
            if (action.payload) {
                const {bids} = action.payload;
                state.ownBids = bids;
                state.ownBidsLastFetchedAmount = bids.length;
            } else {
                state.ownBids = null;
                state.ownBidsLastFetchedAmount = null;
            }
        },
        ownBidsExtended(state, action) {
            const {bids} = action.payload;
            state.ownBids = (state.ownBids || []).concat(bids);
            state.ownBidsLastFetchedAmount = bids.length;
        },
        bidWithdrawn(state, action) {
            const bid = state.ownBids.filter(x => x.id === action.payload)[0];
            bid.can_withdraw = false;
        }
    }
});

export default contentSlice.reducer;
export const {
    allLotsUpdated,
    allLotsExtended,

    ownLotsUpdated,
    ownLotsExtended,

    ownBidsUpdated,
    ownBidsExtended,
    bidWithdrawn
} = contentSlice.actions;