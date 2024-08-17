<template>
	<div>
		<WaitingMatch v-if="store.getters.isAuthenticated && !found"/>
		<div v-else-if="found">
			<Counter321
				:active="found"
				@finished="() => router.push(`multiplayer/${uuid}`)"
				@toggle="(value) => found = value"/>
			<MatchFound :player1="player1" :player2="player2"/>
		</div>
		<div id="must-logged" v-else>
			<h1>You must be logged to play online.</h1>
			<GlowingButton class="go-back-button small-button" :text="'go back'" @click="() => router.go(-1)"/>
		</div>
	</div>
</template>

<script setup>
import Counter321 from '@components/Counter321.vue';
import GlowingButton from '@components/GlowingButton.vue';
import MatchFound from '@components/MatchFound.vue';
import WaitingMatch from '@components/WaitingMatch.vue';
import utils, { makeAuthApiQuery } from '@utils/index';
import router from '@router/index';
import { ref, onMounted, onUnmounted } from 'vue';
import store from '@store';

const found = ref(false);
const player1 = ref('');
const player2 = ref('');
const uuid = ref(undefined);

let global_socket = undefined;

onMounted(() => {
	if (store.getters.isAuthenticated)
	utils.connectToWebsocket('ws/matchmaking/1v1/',
		(/** @type {WebSocket} */ socket) => {
			global_socket = socket;
			socket.onopen = function(e) {
				console.log('[WS] socket connected');
			};
			socket.onclose = function(e) {
				console.log('[WS] socket closed');
			};
			socket.onmessage = function(e) {
				const data = JSON.parse(e.data);
				if (data.type == 'found'){
					socket.close();
					uuid.value = data.uuid;
					found.value = true;
					makeAuthApiQuery('gameinstance/' + uuid.value + '/', 'GET', null,
						(result) => {
							console.log(result.data);
							player1.value = result.data.player_one.username;
							player2.value = result.data.player_two.username;
						},
						(error) => {
							console.log(error);
						}
					)
				}
			};
		},
		(error) => {
			console.log(error);
		}
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
