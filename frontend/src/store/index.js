import { createStore } from 'vuex';
import axios from 'axios';
import { axiosInstance } from '@utils/api';
import audio from './modules/audio';
import { connectToWebsocket } from '@utils/ws';
import pong from './modules/pong';

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

async function updateProfile(context) {
	if (context.state.refreshToken) {
		try {
			const response = await axiosInstance.get('/me/');
			const payload = {
				authUser: response.data.username,
				isAuthenticated: true,
			};
			context.commit('setAuthUser', payload);
			if (!context.state.onlineTrackerWs) {
				connectToWebsocket('ws/onlinetracker/',
					(/** @type {WebSocket} */ websocket) => {
						context.state.onlineTrackerWs = websocket;
						websocket.onerror = (e) => console.log(e)
						websocket.onopen = () => console.debug('[OnlineTracker] open')
						websocket.onclose = () => console.debug('[OnlineTracker] close')
					}
				)
			}
		} catch(error) {
			context.dispatch('deauthentificate'); // Overkill but dont touch lol
		}
	}
}

async function authentificate(context, { access, refresh }) {
	context.commit('updateAccessToken', access);
	context.commit('updateRefreshToken', refresh);

	const ID = parseJwt(access).user_id;
	context.commit('setUserID', ID);

	await context.dispatch('updateProfile');
}

function deauthentificate(context) {
	const payload = {
		authUser: undefined,
		isAuthenticated: false,
	}
	context.commit('setAuthUser', payload);
	context.commit('removeToken');
	context.commit('setUserID', undefined);
}

const theme_colors = {
	green: {
		color: 'hsl(120, 100%, 50%)',
		b_color: 'hsl(120, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(-240deg) contrast(180%) brightness(1.2)',
		mesh_color: '#00ff00',
		image_color: 'sepia(100%) saturate(1000%) hue-rotate(-285deg) contrast(180%) brightness(1.2)',
	},
	red: {
		color: 'hsl(0, 100%, 59%)',
		b_color: 'hsl(0, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(-35deg) contrast(180%) brightness(1.2)',
		mesh_color: '#ff0000',
		image_color: 'sepia(100%) saturate(1000%) hue-rotate(-30deg) contrast(180%) brightness(1.2)',
	},
	yellow: {
		color: 'hsl( 60, 100%, 50%)',
		b_color: 'hsl( 90, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(35deg) contrast(100%) brightness(1.8)',
		mesh_color: '#ffff00',
		image_color: 'sepia(100%) saturate(1000%) hue-rotate(35deg) contrast(100%) brightness(1.8)',
	},
	blue: {
		color: 'hsl(180, 90%,  50%)',
		b_color: 'hsl(180, 100%, 7%)',
		logo_color: 'sepia(100%) saturate(1000%) hue-rotate(-210deg) contrast(120%) brightness(1.8)',
		mesh_color: '#00ffff',
		image_color: 'sepia(100%) saturate(1000%) hue-rotate(-210deg) contrast(120%) brightness(1.8)',
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
	document.documentElement.style.setProperty('--image-filter', color_set.image_color);
}

function loadTheme() {
	const theme = JSON.parse(localStorage.getItem('selected_theme') ?? JSON.stringify('red'));

	changeTheme(theme)
	return (theme);
}

const API_PORT = import.meta.env.DEV ? `:${import.meta.env.VITE_API_PORT}` : window.location.port;

export default createStore({
	modules: {
		audio,
		pong,
	},
	state: {
		onlineTrackerWs: undefined,
		authUser: localStorage.getItem('authUser') ?? {},
		userId: localStorage.getItem('userId'),
		isAuthenticated: JSON.parse(localStorage.getItem('isAuthenticated') ?? 'false'),
		accessToken: localStorage.getItem('accessToken') ?? null,
		refreshToken: localStorage.getItem('refreshToken') ?? null,
		selected_theme: loadTheme(),
		selected_map: localStorage.getItem('selected_map') ?? 'map1',
		map_selector: map_selector,
		endpoints: {
			obtainJWT:  '/token/',
			refreshJWT: "/token/refresh/",
		}
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
		},
		changeSelectedMap(state, map) {
			if (map === 'map1' || map === 'map2') {
				localStorage.setItem('selected_map', map);
				state.selected_map = map;
			}
		}
	},
	actions: {
		updateProfile: updateProfile,
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
		},
		selectedMapPath(state) {
			return state.map_selector[state.selected_map];
		},
		theme(state) {
			const style = document.documentElement.style;

			return (style.getPropertyValue('--glow-color'));
		},
		endpointsBaseURL(state) {
			const protocol = window.location.protocol
				? `${window.location.protocol}//`
				: '';
			const hostname = window.location.hostname;
			const api_base_url = `${import.meta.env.VITE_API_BASE_URL}/`;

			return (`${protocol}${hostname}${API_PORT}${api_base_url}`)
		}
	}
});
