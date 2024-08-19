<template>
	<div>
		<p style="color: red; font-family: sans-serif; font-size: 30px">
			<span>Score: </span><span id="scoreEl">{{ score }}</span>
		</p>
		<canvas ref="gameCanvas"></canvas>
	</div>
</template>

<script>
export default {
	data() {
		return {
			score: 0
		};
	},
	mounted() {
		// Lorsque le composant est monté, on initialise le canvas et le jeu
		this.initializeCanvas();
	},
	methods: {
		initializeCanvas() {
			const canvas = this.$refs.gameCanvas;
			const ctx = canvas.getContext('2d');

			import('@assets/pacman_img/pacman.js').then(module => {
				return module.initialize(ctx, canvas, this.updateScore);
			}).then(() => {
				console.log('Game initialized');
			}).catch(error => {
				console.error('Error initializing game:', error);
			});
		},
		updateScore(newScore) {
			this.score = newScore;
		}
	}
};
</script>

<style scoped>
body {
	margin: 0;
	background-color: black;
}

canvas {
	display: block;
	background: black;
	margin: auto;
}
</style>