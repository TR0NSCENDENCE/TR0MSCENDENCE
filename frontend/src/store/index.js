import { makeAuthApiQuery } from '@utils';
import { createStore } from 'vuex'
import axios from 'axios';

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

async function authentificate(context, {username, password}) {
	let result = undefined;
	let _ = await axios
		.post(context.state.endpoints.obtainJWT, {
			username: username,
			password: password
		})
		.then((response) => {
			context.commit('updateToken', response.data.access);
			// Even though the authentication returned a user object that can be
			// decoded, we fetch it again. This way we aren't super dependant on
			// JWT and can plug in something else.
			makeAuthApiQuery(
				'/me', 'get', {},
				(response) => {
					const payload = {
						authUser: response.data.user.username,
						isAuthenticated: true,
					};
					context.commit('setAuthUser', payload);
				},
				(error) => {
					result = error;
				}
			);
		}).catch((error) => {
			result = error;
		});
	return (result);
}

function deauthentificate(context) {
	const payload = {
		authUser: undefined,
		isAuthenticated: false,
	}
	context.commit('removeToken');
	context.commit('setAuthUser', payload);
}

export default createStore({
	state: {
		authUser: localStorage.getItem('authUser') ?? {},
		isAuthenticated: localStorage.getItem('isAuthenticated') ?? false,
		jwt: localStorage.getItem('token') ?? null,
		endpoints: {
			obtainJWT:  import.meta.env.VITE_API_BASE_URL + 'token/',
			refreshJWT: import.meta.env.VITE_API_BASE_URL + "refresh_token/",
			baseUrl: import.meta.env.VITE_API_BASE_URL + "",
		},
	},
	mutations: {
		setAuthUser(state, { authUser, isAuthenticated }) {
			localStorage.setItem('authUser', authUser);
			localStorage.setItem('isAuthenticated', isAuthenticated);
			state.authUser = authUser;
			state.isAuthenticated = isAuthenticated;
		},
		updateToken(state, newToken) {
			// TODO: For security purposes, take localStorage out of the project.
			localStorage.setItem('token', newToken);
			state.jwt = newToken;
		},
		removeToken(state) {
			// TODO: For security purposes, take localStorage out of the project.
			localStorage.removeItem('token');
			state.jwt = null;
		},
	},
	actions: {
		authentificate: authentificate,
		deauthentificate: deauthentificate
	},
	getters: {
		isAuthenticated(state) {
			return (state.isAuthenticated);
		},
		authUser(state) {
			return (state.authUser);
		}
	}
});
