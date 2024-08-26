import store from "@store";
import { axiosInstance } from "./api";

export function connectToWebsocket(url, onSuccess, onError) {
	axiosInstance.get('/token/ws/')
		.then((response) => onSuccess(new WebSocket(`${store.getters.endpointsBaseURL}${url}?uuid=${response.data.uuid}`)))
		.catch((error) => onError(error))
}

export default { connectToWebsocket };
