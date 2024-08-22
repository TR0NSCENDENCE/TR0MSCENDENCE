<template>
	<div class="canvas">
		<div class="score-header">
			lives: {{ lives }}<br>Score: {{ score }}<br>Time: {{ time }}
		</div>
		<canvas ref="gameCanvas"></canvas>
		<PacmanWin v-if="winOrLose === 2" :score="score" :lives="lives" :time="time" />
		<PacmanGameOver v-if="winOrLose === 1" :score="score" :time="time" />
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import PacmanWin from '@components/PacmanWin.vue';
import PacmanGameOver from '@components/PacmanGameOver.vue';

const score = ref(0);
const lives = ref(3);
const winOrLose = ref(0);
const time = ref('0');

function updateData(newScore, newlives, newTime) {
	score.value = newScore;
	lives.value = newlives;
	time.value = newTime;
}
function initializeCanvas() {
	const canvas = gameCanvas.value;
	const ctx = canvas.getContext('2d');

	function checkWin() {
		import('@assets/pacman_img/1v1.js').then(module => {
			if (module.checkWinOrLose) {
				if (module.checkWinOrLose() === 1)
					winOrLose.value = 1;
				else if (module.checkWinOrLose() === 2)
					winOrLose.value = 2;
				return;
			}
		});
	}

	import('@assets/pacman_img/1v1.js').then(module => {
		return module.initialize(ctx, canvas, updateData, score, checkWin);
	}).then(() => {
		console.log('Game initialized');
	}).catch(error => {
		console.error('Error initializing game:', error);
	});
}

function stopGame() {
	import('@assets/pacman_img/1v1.js').then(module => {
		if (module.stopAnimate) {
			module.stopAnimate();
		}
	});
}

onMounted(() => {
	initializeCanvas();
});

onUnmounted(() => {
	stopGame();
});

const gameCanvas = ref(null);
</script>

<style scoped>
.score-header {
	margin: 3vh;
	color: var(--glow-color);
	font-family: 'SpaceTron';
	font-size: 5vh;
	--size-factor: (0.00188323 * 70vw);
	font-size: calc(12 * var(--size-factor));
	-webkit-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
		0 0 0.45em var(--glow-color);
	-moz-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
		0 0 0.45em var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.canvas {
	display: flex;
}

canvas {
	display: flex;
	background: black;
}
</style>