import { createStore } from "vuex";

export default createStore({
    state: {
        token: '',
        isAuthenticated: false,
        username: '',
        evals: '',
        user: { id: '', username: '', team: '' },
        teams: ''
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token');
                state.isAuthenticated = true;
                state.username = localStorage.getItem('username');
                state.user = localStorage.getItem('user');
            } else {
                state.token = '';
                state.isAuthenticated = false;
                state.username = '';
                state.user = { id: '', username: '', team: '' };
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
        },
        setEvals(state, evals) {
            state.evals = evals;
        },
        removeEvals(state) {
            state.evals = '';
        },
        setUser(state, user) {
            state.user = user;
        },
        removeUser(state) {
            state.user = '';
        },
        setTeams(state, teams) {
            state.teams = teams;
        },
        removeTeams(state) {
            state.teams = '';
        },

    },
    actions: {
        // ...
    },
    modules: {
        // ...
    },
});
