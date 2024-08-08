import store from '@store';
import axios from 'axios';

const	ASSETS_ROOT = new URL('@assets/', import.meta.url) + '/';

function _makeApiQuery(defaults, url, method, payload, onSuccess, onError) {
	const REQUEST_CONFIG = {
		url: url,
		method: method,
		params: payload,
	};
	axios.create(defaults)(REQUEST_CONFIG)
		.then(onSuccess)
		.catch(onError);
}

export function loadAsset(asset) {
	return (ASSETS_ROOT + asset);
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
	loadAsset,
	makeAuthApiQuery,
	makeApiQuery
};

export default utils;
