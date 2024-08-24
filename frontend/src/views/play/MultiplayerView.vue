<template>
	<div>
		<div v-if="store.getters.isAuthenticated">
			<WaitingMatch :match_type="'1v1'" v-if="!found"/>
			<MatchFound v-else
				:player1="player1"
				:player2="player2"
				/>
		</div>
		<div v-else
			id="must-logged"
			>
			<h1> You must be logged to play online. </h1>
			<GlowingButton
				class="go-back-button small-button"
				text="go back"
				@click="() => router.go(-1)"
				/>
		</div>
	</div>
</template>

<script setup>
import GlowingButton from '@components/GlowingButton.vue';
import MatchFound from '@components/MatchFound.vue';
import WaitingMatch from '@components/WaitingMatch.vue';
import router from '@router/index';
import { ref, onMounted, onUnmounted } from 'vue';
import store from '@store';
import { connectToWebsocket } from '@utils/ws';
import { axiosInstance } from '@utils/api';

const defaultUser = {
	user_profile: {
		get_thumbnail: '',
	}
}

const found = ref(false);
const player1 = ref(defaultUser);
const player2 = ref(defaultUser);

let global_socket = undefined;

onMounted(() => {
	if (!store.getters.isAuthenticated)
		return ;
	connectToWebsocket('ws/matchmaking/1v1/',
		(/** @type {WebSocket} */ socket) => {
			global_socket = socket;
			// TODO: Update view if error or premature close ?
			socket.onmessage = (e) => {
				const data = JSON.parse(e.data);
				if (data.type != 'found')
					return ;
				socket.close();
				const uuid = data.uuid;
				axiosInstance.get(`gameinstance/${uuid}/`).then(
					(response) => {
						player1.value = response.data.player_one;
						player2.value = response.data.player_two;
						found.value = true;
					}
				);
				setTimeout(() => router.push(`multiplayer/${uuid}`), 3000);
			};
		},
		(error) => console.log(error)
	);
});

onUnmounted(() => {
	if (global_socket)
		global_socket.close();
});
</script>

<style scoped>
#must-logged
{
	display: flex;
	flex-direction: column;
	align-items: center;
}

h1
{
	color: var(--glow-color);
	margin-top: 10vh;
	text-align: center;
	font-size: 6vh;
	font-weight: bolder;
	letter-spacing: 0.2em;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	position: relative;
}
</style>
