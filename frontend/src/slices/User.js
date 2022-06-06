import {createSlice} from '@reduxjs/toolkit';

const userSlice = createSlice({
    name: 'user',
    initialState: {
        id: null,
        username: null,
        email: null,
        status: null,
        rubles_balance: null,
        profile_photos: null,
    },
    reducers: {
        userDataChanged(state, action) {
            if (action.payload != null) {
                state.id = action.payload.id;
                state.username = action.payload.username;
                state.email = action.payload.email;
                state.status = action.payload.status;
                state.rubles_balance = action.payload.rubles_balance;
                state.profile_photos = action.payload.profile_photos;
            } else {
                state.id = null;
                state.username = null;
                state.email = null;
                state.status = null;
                state.rubles_balance = null;
                state.profile_photos = null;
            }
        }
    }
});

export default userSlice.reducer;
export const {
    userDataChanged
} = userSlice.actions;