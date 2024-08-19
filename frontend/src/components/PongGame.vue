<template>
	<div class="pong_game">
		<div class="pong_game_header">
			<h1 class="pong_game_player">
				player 1: {{ players[0].name }} <br>
				<h3 class="pong_game_commands">commands: 'w + s'</h3>
			</h1>
			<h1 class="pong_game_score_header">
				score: {{ players[0].score }} - {{ players[1].score }}
			</h1>
			<h1 class="pong_game_player">
				player 2: {{ players[1].name }} <br>
				<h3 class="pong_game_commands">commands: '↑ + ↓'</h3>
			</h1>
		</div>
		<div class="pong_game_container">
			<Counter321
				style="width: 100%; height: 10%;"
				:active="counter_is_active"
				@finished="resumeGame"
				@toggle="(value) => counter_is_active = value"
				/>
			<div class="pong_game_canvas_container" style="width: 100%; height: 90%;">
				<canvas ref="pong_game_canvas" style="width: 90%; height:100%;"></canvas>
			</div>
		</div>
		<PauseOverlay v-if="pause_is_active" @resume="resumeGame" />
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';
import { Game } from '@scripts/GameInit.js';
import Counter321 from '@components/Counter321.vue';
import PauseOverlay from '@components/PauseOverlay.vue'
import PongLogic from '@scripts/games/pong/logic';
import PongRenderer from '@scripts/games/pong/renderer';

let game = {
	logic: new PongLogic(),
	renderer: undefined
};

const props = defineProps(['player_1', 'player_2']);
const emits = defineEmits(['onUpdateRequested']);

const counter_is_active = ref(false);
const pong_game_canvas = ref(null);
let pause_is_active = ref(false);

const players = ref([
	{
		name: 'tintin',
		score: 0
	},
	{
		name: 'milou',
		score: 0
	}
]);

function animate() {
	emits('onUpdateRequested')
	game.logic.step();
	game.renderer.render();
	requestAnimationFrame(animate);
}

onMounted(() => {
	const need_resize = () => {
		const canvas = pong_game_canvas.value;
		const width = pong_game_canvas.value.clientWidth;
		const height = pong_game_canvas.value.clientHeight;
		// console.log(width, height, '|', pong_game_canvas.value.width, pong_game_canvas.value.height);

		return (pong_game_canvas.value.width !== width || pong_game_canvas.value.height !== height);
	};

	const get_dims = () => {
		const canvas = pong_game_canvas.value;
		const width = canvas.clientWidth;
		const height = canvas.clientHeight;

		return ({width, height});
	}

	players.value[0].name = props.player_1;
	players.value[1].name = props.player_2;
	game.renderer = new PongRenderer(
		pong_game_canvas.value,
		0xff0000,
		{
			need_resize,
			get_dims
		}
	);
	game.logic.setCallbackUpdateFinished(game.renderer.updateState);
	requestAnimationFrame(animate);
});

onUnmounted(() => {
})

function resumeGame() {
	if (game) {
		counter_is_active.value = false;  // Hide the overlay
		game.resumeGame();
	} else {
		console.error('Game is not initialized');
	}
}

defineExpose({
	setters: {
		ball: game.logic.setBall,
		paddle_1: game.logic.setPaddle1,
		paddle_2: game.logic.setPaddle2
	}
})

</script>

<style scoped>
@font-face {
	font-family: 'SpaceTron';
	src: url('/fonts/spacetron-51nwz.otf') format('opentype');
	font-weight: normal;
	font-style: normal;
}

.pong_game {
	height: 100%;
	width: 100%;
}

.pong_game_header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 10px;
	color: var(--glow-color);
	height: 10%;
	width: 100%;
	font-family: 'SpaceTron', sans-serif;
}

.pong_game_container {
	height: 90%;
	width: 100%;
}

.pong_game_canvas_container {
	display: flex;
	align-items: center;
	justify-content: center;
}

.pong_game_player,
.pong_game_score_header {
	flex: 1;
	text-align: center;
	padding: 10px;
}

.pong_game_commands {
	font-size: 0.5em;
}
</style>
