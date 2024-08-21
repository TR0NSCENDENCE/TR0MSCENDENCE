<template>
	<div class="canvas">
		<p class="score-header">
			<span>Score: </span><span id="scoreEl">{{ score }}</span>
		</p>
		<canvas ref="gameCanvas"></canvas>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const score = ref(0);

function updateScore(newScore) {
	score.value = newScore;
}

function initializeCanvas() {
	const canvas = gameCanvas.value;
	const ctx = canvas.getContext('2d');

	import('@assets/pacman_img/1v1.js').then(module => {
		return module.initialize(ctx, canvas, updateScore, score);
	}).then(() => {
		console.log('Game initialized');
	}).catch(error => {
		console.error('Error initializing game:', error);
	});
}

function stopGame() {
    // Si le module pacman a des méthodes spécifiques pour nettoyer le jeu, vous pouvez les appeler ici
    import('@assets/pacman_img/1v1.js').then(module => {
        if (module.stopAnimate) {
            module.stopAnimate(); // Appeler une méthode d'arrêt si elle existe
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
	text-align: center;
	color: var(--glow-color);
	font-family: 'SpaceTron';
	font-size: 5vh;
	transform: translateY(-1em);
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
	display: block;
	background: black;
	margin: auto;
}
</style>