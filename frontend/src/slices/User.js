import {createSlice} from '@reduxjs/toolkit';

const userSlice = createSlice({
    name: 'user',
    initialState: {
        id: undefined,
        username: undefined,
        email: undefined,
        status: undefined,
        rubles_balance: undefined,
        profile_photos: undefined,
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
                state.id = undefined;
                state.username = undefined;
                state.email = undefined;
                state.status = undefined;
                state.rubles_balance = undefined;
                state.profile_photos = undefined;
            }
        }
    }
});

export default userSlice.reducer;
export const {
    userDataChanged
} = userSlice.actions;