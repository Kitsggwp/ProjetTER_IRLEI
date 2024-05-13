import { createStore } from "vuex";

export default createStore({
    state: {
        token: '',
        isAuthenticated: false,
        username: ''
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token');
                state.isAuthenticated = true;
                state.username = localStorage.getItem('username');
            } else {
                state.token = '';
                state.isAuthenticated = false;
                state.username = '';
            }
        },
        setToken(state, { token, username }) {
            state.token = token;
            state.isAuthenticated = true;
            state.username = username;
            localStorage.setItem('username', username);
        },
        removeToken(state) {
            state.token = '';
            state.isAuthenticated = false;
            state.username = '';
            localStorage.removeItem('username');
        }
    },
    actions: {
        // ...
    },
    modules: {
        // ...
    },
});
