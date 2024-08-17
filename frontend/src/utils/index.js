import store from '@store';
import axios from 'axios';

function _makeApiQuery(defaults, url, method, payload, onSuccess, onError) {
	const REQUEST_CONFIG = method.toUpperCase() === 'POST'
		? {
			url: url,
			method: method,
			data: payload,
		}
		: {
			url: url,
			method: method,
			params: payload,
		};
	axios.create(defaults)(REQUEST_CONFIG)
		.then(onSuccess)
		.catch(onError);
}

export function connectToWebsocket(url, onSuccess, onError) {
	makeAuthApiQuery('token/ws/', 'GET', null,
		(result) => {
			const uuid = result.data.uuid;
			onSuccess(new WebSocket(store.state.endpoints.baseUrl + url + '?uuid=' + uuid));
		},
		onError
	)
}

export function makeAuthApiQuery(url, method, payload, onSuccess, onError) {
	const DEFAULTS = {
		baseURL: store.state.endpoints.baseUrl,
		headers: {
			Authorization: `Bearer ${store.state.jwt}`,
			'Content-Type': 'application/json',
		},
		xhrFields: {
			withCredentials: true,
		}
	};
	_makeApiQuery(DEFAULTS, url, method, payload, onSuccess, onError);
}

export function makeApiQuery(url, method, payload, onSuccess, onError) {
	const DEFAULTS = {
		baseURL: store.state.endpoints.baseUrl,
		headers: {
			'Content-Type': 'application/json',
		},
		xhrFields: {
			withCredentials: false,
		}
	};
	_makeApiQuery(DEFAULTS, url, method, payload, onSuccess, onError);
}

const utils = {
	makeAuthApiQuery,
	makeApiQuery,
	connectToWebsocket
};

export default utils;
