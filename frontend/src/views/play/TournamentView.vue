<template>

</template>

<script setup>
import router from '@router/index';
import { axiosInstance } from '@utils/api';
import { connectToWebsocket } from '@utils/ws';
import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const ws_error = ref(false);
const connected = ref(false);

const route = useRoute();
const UUID = route.params.uuid;

let global_socket = undefined;

const setup = async (/** @type {WebSocket} */ socket) => {
	global_socket = socket;

	socket.onopen = () => {
		console.log('[WS] socket connected');
	};
	socket.onclose = (e) => {
		console.log('[WS] socket closed');
		if (!e.wasClean)
			ws_error.value = true;
		console.log(e);
	};
	socket.onerror = (e) => {
		console.log('[WS] socket error');
		ws_error.value = true;
		console.log(e);
	}
	socket.onmessage = (e) => {
		console.log(e);
	}
	try {
		const response = await axiosInstance.get(`tournamentinstance/${UUID}/`);

	} catch (e) {
		console.log(e);
		socket.close();
		return;
	}
	connected.value = true;
};

onMounted(() => {
	connectToWebsocket(`ws/tournamentinstance/${UUID}/`,
		setup,
		(error) => {
			router.push('/');
			console.log(error)
		}
	);
});

onUnmounted(() => {
	if (global_socket)
		global_socket.close();
});
</script>
