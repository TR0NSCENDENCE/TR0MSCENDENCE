<template>
	<div>
		<div v-if="store.getters.isAuthenticated">
			<div v-if="ws_error">
				<h1> A server error occured... </h1>
				<GlowingButton text="main menu" dest="/" />
			</div>
			<div v-else-if="connected">
				<div v-if="game_running">
					<GameOponentsBar
						:player_1="players[0]"
						:player_2="players[1]"/>
					<PongGame
						ref="game"
						@onUpdateRequested="update"/>
				</div>
				<MatchWon
					v-else
					:winner="winner"
					:loser="loser"
					/>
			</div>
			<h1 v-else> Waiting for connection... </h1>
		</div>
		<div id="must-logged" v-else>
			<h1>You must be logged to play online.</h1>
			<GlowingButton class="go-back-button small-button" text="go back" dest="/play'"/>
		</div>
	</div>
</template>

<script setup>
import PongGame from '@components/PongGame.vue';
import GlowingButton from '@components/GlowingButton.vue';
import store from '@store';
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router'
import { connectToWebsocket } from '@utils/ws';
import router from '@router/index';
import { KEYBOARD } from '@scripts/KeyboardManager';
import { axiosInstance } from '@utils/api';
import GameOponentsBar from '@components/GameOponentsBar.vue';
import MatchWon from './MatchWon.vue';

let /** @type {WebSocket} */ global_socket = undefined;
let p1 = undefined;
const connected = ref(false);
const game = ref(null);
const ws_error = ref(false)

const default_player = {
	score: 0,
	user: {
		username: undefined,
		user_profile: {
			get_thumbnail: undefined,
		},
	},
};

const players = ref([
	// structuredClone to avoid referencing
	structuredClone(default_player),
	structuredClone(default_player)
]);
const winner = ref('');
const loser = ref('');
const game_running = ref(true);

const VELOCITY = 0.4;

const route = useRoute();
const UUID = route.params.uuid;
const inversed = () => p1 === parseInt(store.getters.userId);

const update = () => {
	let offset = 0;

	if (KEYBOARD.isKeyDown('ArrowRight') || KEYBOARD.isKeyDown('d'))
		offset -= 1;
	if (KEYBOARD.isKeyDown('ArrowLeft') || KEYBOARD.isKeyDown('a'))
		offset += 1;
	if (offset != 0) {
		global_socket.send(JSON.stringify({
			type: 'player_move',
			payload: {
				offset: VELOCITY * (inversed() ? -offset : offset)
			}
		}));
	}
};

const setup = async (/** @type {WebSocket} */ socket) => {
	global_socket = socket;

	socket.onopen = () => {
		console.log('[WS] socket connected');
	};
	socket.onclose = (e) => {
		console.log('[WS] socket closed');
		if (!e.wasClean)
			ws_error.value = true;
		console.log(e)
	};
	socket.onerror = (e) => {
		console.log('[WS] socket error');
		ws_error.value = true;
		console.log(e)
	}
	socket.onmessage = (e) => {
		const event = JSON.parse(e.data);

		if (event.type === 'sync') {
			let state = event.state;

			if (inversed()) {
				state.ball.position = {
					x: -state.ball.position.x,
					y: -state.ball.position.y,
				};
				state.ball.velocity = {
					x: -state.ball.velocity.x,
					y: -state.ball.velocity.y,
				};
				state.paddle_1.position = {
					x: -state.paddle_1.position.x,
					y: -state.paddle_1.position.y
				};
				state.paddle_2.position = {
					x: -state.paddle_2.position.x,
					y: -state.paddle_2.position.y
				};
			}
			game.value.setters.ball(state.ball.position, state.ball.velocity);
			game.value.setters.paddle_1(state.paddle_1.position);
			game.value.setters.paddle_2(state.paddle_2.position);
		} else if (event.type === 'score') {
			players.value[0].score = event.scores.p1;
			players.value[1].score = event.scores.p2;
		} else if (event.type === 'winner') {
			const winner_id = event.winner_id;
			const has_won = store.getters.userId == winner_id;
			const winner_index = has_won ^ inversed() ? 1 : 0;

			game_running.value = false;
			winner.value = players.value[winner_index].user.username;
			loser.value = players.value[1 - winner_index].user.username;
		}
	}
	try {
		const response = await axiosInstance.get(`gameinstance/${UUID}/`);

		players.value[0].user = response.data.player_one;
		players.value[1].user = response.data.player_two;
		p1 = response.data.player_one.pk;
	} catch(e) {
		console.log(e);
		socket.close();
		return ;
	}
	connected.value = true;
};

onMounted(() => {
	connectToWebsocket(`ws/gameinstance/${UUID}/`,
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
#must-logged {
	display: flex;
	flex-direction: column;
	align-items: center;
}

h1 {
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
