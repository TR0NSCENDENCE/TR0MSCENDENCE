import { createStore } from 'vuex';
import axios from 'axios';
import { axiosInstance } from '@utils/api';

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

function parseJwt (token) {
	var base64Url = token.split('.')[1];
	var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
	var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
		return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
	}).join(''));

	return JSON.parse(jsonPayload);
}

async function authentificate(context, { username, password }) {
	let result = undefined;
	let _ = await axiosInstance
		.post(context.state.endpoints.obtainJWT, {
			username: username,
			password: password
		})
		.then((response) => {
			context.commit('updateAccessToken', response.data.access);
			context.commit('updateRefreshToken', response.data.refresh);
			// Even though the authentication returned a user object that can be
			// decoded, we fetch it again. This way we aren't super dependant on
			// JWT and can plug in something else.

			const ID = parseJwt(response.data.access).user_id;
			context.commit('setUserID', ID);

			axiosInstance.get('/me/').then(
				(response) => {
					const payload = {
						authUser: response.data.username,
						isAuthenticated: true,
					};
					context.commit('setAuthUser', payload);
				}
			).catch((error) => console.log(error));
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
	context.commit('setUserID', undefined);
}

const theme_colors = {
	green: {
		color: 'hsl(120, 100%, 50%)',
		b_color: 'hsl(120, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(-240deg) contrast(180%) brightness(1.2)',
		mesh_color: '#00ff00',
	},
	red: {
		color: 'hsl(0, 100%, 59%)',
		b_color: 'hsl(0, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(-35deg) contrast(180%) brightness(1.2)',
		mesh_color: '#ff0000'
	},
	yellow: {
		color: 'hsl( 60, 100%, 50%)',
		b_color: 'hsl( 90, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(35deg) contrast(100%) brightness(1.8)',
		mesh_color: '#ffff00'
	},
	blue: {
		color: 'hsl(180, 90%,  50%)',
		b_color: 'hsl(180, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(-210deg) contrast(120%) brightness(1.8)',
		mesh_color: '#00ffff'
	},
}

function changeTheme(theme) {
	const color_set = theme_colors[theme];

	document.documentElement.style.setProperty('--glow-color', color_set.color);
	document.documentElement.style.setProperty('--background-color', color_set.b_color);
	document.documentElement.style.setProperty('--logo-filter', color_set.logo_color);
	document.documentElement.style.setProperty('--mesh-color', color_set.mesh_color);
}

function loadTheme() {
	const theme = JSON.parse(localStorage.getItem('selected_theme') ?? JSON.stringify('red'));

	changeTheme(theme)
	return (theme);
}

export default createStore({
	state: {
		authUser: localStorage.getItem('authUser') ?? {},
		userId: localStorage.getItem('userId'),
		isAuthenticated: JSON.parse(localStorage.getItem('isAuthenticated') ?? 'false'),
		accessToken: localStorage.getItem('accessToken') ?? null,
		refreshToken: localStorage.getItem('refreshToken') ?? null,
		selected_theme: loadTheme(),
		endpoints: {
			obtainJWT:  'token/',
			refreshJWT: "token/refresh",
			baseUrl: import.meta.env.VITE_API_BASE_URL + "/",
		},
	},
	mutations: {
		setUserID(state, id) {
			localStorage.setItem('userId', id);
			state.userId = id;
		},
		setAuthUser(state, { authUser, isAuthenticated }) {
			localStorage.setItem('authUser', authUser);
			localStorage.setItem('isAuthenticated', JSON.stringify(isAuthenticated));
			state.authUser = authUser;
			state.isAuthenticated = isAuthenticated;
		},
		updateRefreshToken(state, newToken) {
			localStorage.setItem('refreshToken', newToken);
			state.refreshToken = newToken;
		},
		updateAccessToken(state, newToken) {
			// TODO: For security purposes, take localStorage out of the project.
			localStorage.setItem('accessToken', newToken);
			state.accessToken = newToken;
		},
		removeToken(state) {
			// TODO: For security purposes, take localStorage out of the project.
			localStorage.removeItem('accessToken');
			localStorage.removeItem('refreshToken');
			state.accessToken = null;
			state.refreshToken = null;
		},
		changeSelectedTheme(state, theme) {
			if (theme === 'red'
				|| theme === 'blue'
				|| theme === 'yellow'
				|| theme === 'green'
			) {
				localStorage.setItem('selected_theme', JSON.stringify(theme));
				state.selected_theme = theme;
				changeTheme(theme);
			}
		}
	},
	actions: {
		authentificate: authentificate,
		deauthentificate: deauthentificate
	},
	getters: {
		userId(state) {
			return (state.userId);
		},
		accessToken(state) {
			return (state.accessToken);
		},
		refreshToken(state) {
			return (state.refreshToken);
		},
		isAuthenticated(state) {
			return (state.isAuthenticated);
		},
		authUser(state) {
			return (state.authUser);
		},
		selectedTheme(state) {
			return (state.selected_theme);
		}
	}
});
