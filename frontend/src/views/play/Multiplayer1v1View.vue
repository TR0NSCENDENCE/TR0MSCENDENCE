<template>
	<div>
		<PongGame v-if="store.getters.isAuthenticated" :config="config" />
		<div id="must-logged" v-else>
			<h1>You must be logged to play online.</h1>
			<GlowingButton class="go-back-button small-button" :text="'go back'" :dest="'/play'"/>
		</div>
	</div>
</template>

<script setup>
import PongGame from '@components/PongGame.vue';
import { config } from '@assets/game_config/pong/solo';
import GlowingButton from '@components/GlowingButton.vue';
import store from '@store';
import { onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router'
import utils from '@utils/index';

let global_socket = undefined;

const route = useRoute();

onMounted(() => {
	utils.connectToWebsocket(`ws/gameinstance/${route.params.uuid}/`,
		(/** @type {WebSocket} */ socket) => {
			global_socket = socket;
			socket.onopen = (e) => {
				console.log('[WS] socket connected');
				socket.send(JSON.stringify({'type': 'test-position-update'}));
			}
			socket.onclose = (e) => console.log('[WS] socket closed');
			socket.onmessage = (e) => console.log(e.data);
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
