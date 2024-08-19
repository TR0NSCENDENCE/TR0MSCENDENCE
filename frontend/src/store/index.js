import { makeAuthApiQuery } from '@utils';
import { createStore } from 'vuex'
import axios from 'axios';

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

async function authentificate(context, { username, password }) {
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
				'/me/', 'get', {},
				(response) => {
					const payload = {
						authUser: response.data.username,
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

const map_selector = {
	map1: '/ressources/map_scene/TronStadiumUltimo.glb',
	map2: '/ressources/map_scene/TronscendenceMap2.glb'
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
		isAuthenticated: JSON.parse(localStorage.getItem('isAuthenticated') ?? 'false'),
		jwt: localStorage.getItem('token') ?? null,
		selected_theme: loadTheme(),
		selected_map: localStorage.getItem('selected_map') ?? 'map1',
		map_selector: map_selector,
		endpoints: {
			obtainJWT: import.meta.env.VITE_API_BASE_URL + 'token/',
			refreshJWT: import.meta.env.VITE_API_BASE_URL + "refresh_token/",
			baseUrl: import.meta.env.VITE_API_BASE_URL + "",
		}
	},
	mutations: {
		setAuthUser(state, { authUser, isAuthenticated }) {
			localStorage.setItem('authUser', authUser);
			localStorage.setItem('isAuthenticated', JSON.stringify(isAuthenticated));
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
		},
		changeSelectedMap(state, map) {
			if (map === 'map1' || map === 'map2') {
				localStorage.setItem('selected_map', map);
				state.selected_map = map;
			}
		}
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
		},
		selectedTheme(state) {
			return (state.selected_theme);
		},
		selectedMapPath(state) {
			return state.map_selector[state.selected_map];
		}
	}
});
