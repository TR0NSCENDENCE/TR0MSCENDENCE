<template>
	<div class="tournament-matchmaking" v-if="store.getters.isAuthenticated">
		<WaitingMatch :match_type="'tournament'" v-if="!found" />
		<div class="tournament" v-else>
			<h1>Tournament</h1>
			<Bracket :tournamentdata="tournament" />
		</div>
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
</template>

<script setup>
import Bracket from '@/components/TournamentBracket.vue';
import GlowingButton from '@components/GlowingButton.vue';
import WaitingMatch from '@components/WaitingMatch.vue';
import router from '@router/index';
import store from '@store';
import { axiosInstance } from '@utils/api';
import { connectToWebsocket } from '@utils/ws';
import { onMounted, onUnmounted, ref } from 'vue';

const defaultUser = {
	user_profile: {
		get_thumbnail: '',
	}
}

const found = ref(false);
const tournament = ref();

let global_socket = undefined;

onMounted(() => {
	if (!store.getters.isAuthenticated)
		return ;
	connectToWebsocket('ws/matchmaking/tournament/',
		(/** @type {WebSocket} */ socket) => {
			global_socket = socket;
			// TODO: Update view if error or premature close ?
			socket.onmessage = (e) => {
				const data = JSON.parse(e.data);
				if (data.type != 'found')
					return ;
				const uuid = data.uuid;
				router.push(`tournament/${uuid}`);
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
#must-logged {
	display: flex;
	flex-direction: column;
	align-items: center;
}

#must-logged > h1 {
	color: var(--glow-color);
	margin-top: 10vh;
	text-align: center;
	font-size: 6vh;
	font-weight: bolder;
	letter-spacing: 0.2em;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	position: relative;

}

.tournament {
	display: flex;
	flex-direction: column;
	align-items: center;
	color: var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}
</style>
