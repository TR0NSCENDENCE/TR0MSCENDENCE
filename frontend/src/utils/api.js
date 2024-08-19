import store from "@store";
import axios from "axios";

const axiosInstance = axios.create({
	headers: {
		"Content-Type": "application/json",
	},
	xhrFields: {
		withCredentials: false,
	}
});

const setupInstance = () => {
	axiosInstance.interceptors.request.use(
		(config) => {
			const token = store.getters.accessToken;
			config.baseURL = store.state.endpoints.baseUrl;
			if (token) {
				config.headers['Authorization'] = `Bearer ${token}`
				config.withCredentials = true;
			} else {
				config.withCredentials = false;
			}
			return config;
		},
		(error) => {
			return Promise.reject(error);
		}
	)
	axiosInstance.interceptors.response.use(
		(res) => {return res},
		async (err) => {
			const originalConfig = err.config;
			if (err.response && err.response.status === 401 && !originalConfig._retry) {
				originalConfig._retry = true;
				try {
					const rs = await axiosInstance.post("/token/refresh/", {
						refresh: store.getters.refreshToken,
					})

					const { access } = rs.data;

					store.commit('updateAccessToken', access);

					return axiosInstance(originalConfig);
				} catch (_error) {
					return Promise.reject(_error);
				}
			}
			return Promise.reject(err);
		}
	)
}

export { axiosInstance, setupInstance };