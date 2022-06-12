import {createSlice} from '@reduxjs/toolkit';

const userSlice = createSlice({
    name: 'user',
    initialState: {
        id: null,
        username: null,
        email: null,
        status: null,
        rublesBalance: null,
        profilePhotos: null,
    },
    reducers: {
        userDataChanged(state, action) {
            if (action.payload != null) {
                state.id = action.payload.id;
                state.username = action.payload.username;
                state.email = action.payload.email;
                state.status = action.payload.status;
                // noinspection JSUnresolvedVariable
                state.rublesBalance = action.payload.rubles_balance;
                // noinspection JSUnresolvedVariable
                state.profilePhotos = action.payload.profile_photos;
            } else {
                state.id = null;
                state.username = null;
                state.email = null;
                state.status = null;
                state.rublesBalance = null;
                state.profilePhotos = null;
            }
        },
        balanceChanged(state, action) {
            state.rublesBalance = action.payload;
        }
    }
});

export default userSlice.reducer;
export const {
    userDataChanged,
    balanceChanged

} = userSlice.actions;