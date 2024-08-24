<template>
	<div id="tournament-view">
		<Counter321 ref="counter"/>
		<TournamentBracket :tournamentdata="tournament" v-if="tournament"/>
	</div>
</template>

<script setup>
import Counter321 from '@components/Counter321.vue';
import TournamentBracket from '@components/TournamentBracket.vue';
import router from '@router/index';
import { axiosInstance } from '@utils/api';
import { connectToWebsocket } from '@utils/ws';
import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const ws_error = ref(false);
const connected = ref(false);
const tournament = ref(null);
const counter = ref(null);

const route = useRoute();
const UUID = route.params.uuid;

let global_socket = undefined;

const setup = async (/** @type {WebSocket} */ socket) => {
	global_socket = socket;

	try {
		const response = await axiosInstance.get(`tournamentinstance/${UUID}/`);
		tournament.value = response.data
	} catch (e) {
		console.log(e);
		socket.close();
		return;
	}
	socket.onclose = (e) => {
		if (!e.wasClean)
			ws_error.value = true;
		console.log(e);
	};
	socket.onerror = (e) => {
		ws_error.value = true;
		console.log(e);
	}
	socket.onmessage = (e) => {
		const data = JSON.parse(e.data);
		if (data.type == 'match_start') {
			const match_uuid = data.match_uuid;
			counter.value.start();
			setTimeout(() => router.push(`/play/multiplayer/${match_uuid}?redirect=${window.location.pathname}`), 3000);
		}
		if (data.type == 'tournament_update') {
			const tournament_data = data.tournament_data;
			tournament.value = tournament_data;
		}
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

<style scoped>
#tournament-view {
	display: flex;
	flex-direction: column;
	align-items: center;
}
</style>
