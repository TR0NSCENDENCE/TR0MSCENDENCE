<template>
	<div>
		<div v-if="store.getters.isAuthenticated">
			<div v-if="error" style="display: flex; flex-direction: column; align-items: center;">
				<h1> A server error occured... </h1>
				<GlowingButton
					text="main menu"
					dest="/"
					/>
			</div>
			<div v-else-if="winner">
				<MatchWon
					:winner="winner"
					:loser="loser"
					/>
			</div>
			<div v-else-if="ws_connected">
				<div v-if="game_running">
					<GameOponentsBar
						:player_1="players[0]"
						:player_2="players[1]"
						/>
					<PongGame
						:render_config="config_multiplayer"
						:enable_simulation="false"
						@onUpdateRequested="onUpdateRequested"
						ref="game"
						/>
				</div>
			</div>
			<h1 v-else> Waiting for connection... </h1>
		</div>
		<div v-else id="must-logged">
			<h1> You must be logged to play online. </h1>
			<GlowingButton
				class="go-back-button small-button"
				text="go back"
				dest="/play"
				/>
		</div>
	</div>
</template>

<script setup>
import { config_multiplayer } from '@assets/game/pong/render_config.json'
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
import { Direction } from '@scripts/games/pong/utils';

let /** @type {WebSocket} */ global_socket = undefined;
let p1 = undefined;
const game = ref(null);
const error = ref(false);
const ws_connected = ref(false);
const game_running = ref(true);

const default_player = Object.freeze({
	score: 0,
	user: {
		username: undefined,
		user_profile: {
			get_thumbnail: undefined,
		},
	},
});

const players = ref([
	structuredClone(default_player),
	structuredClone(default_player)
]);
const winner = ref(null);
const loser = ref(null);

const route = useRoute();
const UUID = route.params.uuid;
const inversed = () => p1 === parseInt(store.getters.userId);

let player_one_dir = {
	right: false,
	left: false
};

let player_two_dir = {
	right: false,
	left: false
};

const onUpdateRequested = () => {
	const dir = {
		right: KEYBOARD.isKeyDown('ArrowRight') || KEYBOARD.isKeyDown('d'),
		left: KEYBOARD.isKeyDown('ArrowLeft') || KEYBOARD.isKeyDown('a')
	};

	if (dir === player_one_dir)
		return ;
	player_one_dir = dir;
	global_socket.send(JSON.stringify({
		type: 'player_direction',
		payload: dir
	}));
	const direction = (dir.left ? -1 : 0) + (dir.right ? 1 : 0);
	store.commit('pong/set_player_direction', {id: inversed() ? 0 : 1, direction: direction});
}

const setup = (/** @type {WebSocket} */ socket) => {
	global_socket = socket;

	socket.onopen = () => {
		ws_connected.value = true;
	};
	socket.onclose = (e) => {
		ws_connected.value = false;
		if (!e.wasClean)
			error.value = true;
	};
	socket.onerror = (e) => {
		error.value = true;
		console.log(e);
	}
	socket.onmessage = (e) => {
		const event = JSON.parse(e.data);

		if (!game.value)
			return ;

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
				state.paddles[0].position = {
					x: -state.paddles[0].position.x,
					y: -state.paddles[0].position.y
				};
				state.paddles[1].position = {
					x: -state.paddles[1].position.x,
					y: -state.paddles[1].position.y
				};
			}
			game.value.forceUpdate({
				ball: state.ball,
				paddles: [
					state.paddles[0],
					state.paddles[1]
				]
			});
		} else if (event.type === 'score') {
			players.value[0].score = event.scores.p1;
			players.value[1].score = event.scores.p2;
		} else if (event.type === 'counter_start') {
			game.value.onCountdownStart();
		} else if (event.type === 'counter_stop') {
			game.value.onCountdownStop();
		} else if (event.type === 'winner') {
			const winner_id = event.winner_id;
			const has_won = store.getters.userId == winner_id;
			const winner_index = has_won ^ inversed() ? 1 : 0;

			winner.value = players.value[winner_index].user.username;
			loser.value = players.value[1 - winner_index].user.username;
			game_running.value = false;
			if (route.query.redirect)
				setTimeout(() => router.push(route.query.redirect), 4000);
		}
	}
};

onMounted(async () => {
	try {
		const response = await axiosInstance.get(`gameinstance/${UUID}/`);
		players.value[0].user = response.data.player_one;
		players.value[1].user = response.data.player_two;
		p1 = response.data.player_one.pk;
	} catch (e) {
		console.log(e);
		error.value = true;
		return ;
	}
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
