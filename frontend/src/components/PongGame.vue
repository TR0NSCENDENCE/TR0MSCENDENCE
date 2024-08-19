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
		<div>
			<Counter321 :active="counter_is_active" @finished="resumeGame"
				@toggle="(value) => counter_is_active = value" />
			<div class="pong_game_container" ref="pong_game_container"></div>
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

let renderer = undefined;
let game = undefined;

const props = defineProps(['config'])

const counter_is_active = ref(false);
const pong_game_container = ref(null);
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
	if (!game.isGamePaused()) {
		game.update();
		players.value[0].score = game.getScore1();
		players.value[1].score = game.getScore2();
	}
	game.render();
	requestAnimationFrame(animate);
}

onMounted(() => {
	renderer = new THREE.WebGLRenderer({ antialias: true });
	renderer.setSize(window.innerWidth * 0.9, window.innerHeight * 0.9);
	pong_game_container.value.appendChild(renderer.domElement);
	game = new Game(counter_is_active, () => pause_is_active.value = true, () => pause_is_active.value = false, props.config, renderer);
	game.countdown();
	requestAnimationFrame(animate);
});

onUnmounted(() => {
	if (renderer !== undefined)
		renderer.dispose();
})

function resumeGame() {
	if (game) {
		counter_is_active.value = false;  // Hide the overlay
		game.resumeGame();
	} else {
		console.error('Game is not initialized');
	}
}

</script>

<style scoped>
@font-face {
	font-family: 'SpaceTron';
	src: url('/fonts/spacetron-51nwz.otf') format('opentype');
	font-weight: normal;
	font-style: normal;
}

.pong_game_header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 10px;
	color: var(--glow-color);
	height: 10vh;
	font-family: 'SpaceTron', sans-serif;
}

.pong_game_container {
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

/* .pong_game_container {
	border: 2px solid red;
} */

.pong_game_commands {
	font-size: 0.5em;
}
</style>
