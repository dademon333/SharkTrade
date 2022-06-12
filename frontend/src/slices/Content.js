import {createSlice} from '@reduxjs/toolkit';

const contentSlice = createSlice({
    name: 'content',
    initialState: {
        allLots: null,
        allLotsLastFetchedAmount: null,

        ownLots: null,
        ownLotsLastFetchedAmount: null,

        ownBids: null,
        ownBidsLastFetchedAmount: null,

        ownItems: null,
        ownItemsLastFetchedAmount: null,

        lotPageLotsData: {},
        itemPageItemsData: {}
    },
    reducers: {
        allContentCleared(state) {
            state.allLots = null;
            state.allLotsLastFetchedAmount = null;

            state.ownLots = null;
            state.ownLotsLastFetchedAmount = null;

            state.ownBids = null;
            state.ownBidsLastFetchedAmount = null;

            state.ownItems = null;
            state.ownItemsLastFetchedAmount = null;

            state.lotPageLotsData = {};
            state.itemPageItemsData = {};
        },

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
            const {lots} = action.payload;
            state.ownLots = lots;
            state.ownLotsLastFetchedAmount = lots.length;
        },
        ownLotsExtended(state, action) {
            const {lots} = action.payload;
            state.ownLots = (state.ownLots || []).concat(lots);
            state.ownLotsLastFetchedAmount = lots.length;
        },

        ownBidsUpdated(state, action) {
            const {bids} = action.payload;
            state.ownBids = bids;
            state.ownBidsLastFetchedAmount = bids.length;
        },
        ownBidsExtended(state, action) {
            const {bids} = action.payload;
            state.ownBids = (state.ownBids || []).concat(bids);
            state.ownBidsLastFetchedAmount = bids.length;
        },
        bidWithdrawn(state, action) {
            const bid = state.ownBids.filter(x => x.id === action.payload)[0];
            bid.can_withdraw = false;
        },

        ownItemsUpdated(state, action) {
            const {items} = action.payload;
            state.ownItems = items;
            state.ownItemsLastFetchedAmount = items.length;
        },
        ownItemsExtended(state, action) {
            const {items} = action.payload;
            state.ownItems = (state.ownItems || []).concat(items);
            state.ownItemsLastFetchedAmount = items.length;
        },

        lotPageLotDataChanged(state, action) {
            const {lot, lotId} = action.payload;
            state.lotPageLotsData[lotId] = lot;
        },
        itemPageItemDataChanged(state, action) {
            const {item, itemId} = action.payload;
            state.itemPageItemsData[itemId] = item;
        }
    }
});

export default contentSlice.reducer;
export const {
    allContentCleared,

    allLotsUpdated,
    allLotsExtended,

    ownLotsUpdated,
    ownLotsExtended,

    ownBidsUpdated,
    ownBidsExtended,
    bidWithdrawn,

    ownItemsUpdated,
    ownItemsExtended,

    lotPageLotDataChanged,
    itemPageItemDataChanged,
} = contentSlice.actions;