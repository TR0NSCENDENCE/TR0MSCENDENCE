import store from "@store";
import { axiosInstance } from "./api";

export function connectToWebsocket(url, onSuccess, onError) {
	axiosInstance.get('/token/ws/').then(
		(response) => {
			const uuid = response.data.uuid;
			onSuccess(new WebSocket(store.state.endpoints.baseUrl + url + '?uuid=' + uuid));
		}
	).catch(
		(error) => onError(error)
	);
}

export default { connectToWebsocket };
