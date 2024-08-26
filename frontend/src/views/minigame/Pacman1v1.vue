<template>
	<div class="canvas">
		<div class="score-header">
			<div class="score-line">
				lives: <br> {{ lives }}
			</div>
			<div class="score-line">
				Score: <br> {{ score }}
			</div>
			<div class="score-line">
				Time: <br> {{ time }}
			</div>
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
import store from '@store';
import { axiosInstance } from '@utils/api';

const score = ref(0);
const lives = ref(3);
const winOrLose = ref(0);
const time = ref('0');

const gameStat = {
	score:  0,
	time: 0,
	status: 'lose',
	mode: '',
};

function updateData(newScore, newlives, newTime) {
	score.value = newScore;
	lives.value = newlives;
	time.value = newTime;
}

function _saveUserData() {
	axiosInstance.get('/me/pacman-data/').then(
		(res) => {
			let data = res.data;
			if (!data.pacman_data)
				data.pacman_data = [];
			data.pacman_data.push(gameStat);
			axiosInstance.put('/me/pacman-data/', data).catch(
				(e) => console.log(e)
			)
		}
	).catch(
		(e) => console.log(e)
	)
}

function _saveLocalData() {
	let data = JSON.parse(localStorage.getItem('stats')) || [];
	data.push(gameStat);
	localStorage.setItem('stats', JSON.stringify(data));
}

function saveData(score, time, winOrLose) {
	gameStat.score = score;
	gameStat.time = time;
	gameStat.status = winOrLose === 2 ? 'win' : 'lose';
	gameStat.mode = '1v1';
	if (store.getters.isAuthenticated)
		_saveUserData();
	else
		_saveLocalData();
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
	saveData(score.value, time.value, winOrLose.value);
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
.canvas {
	display: flex;
	flex-direction: row;
	width: 70vw;
	height: 70vh;
	box-sizing: border-box;
	justify-content: space-between;
	gap: 8vw;
}

.score-header {
	margin: 3vh 15vw;
	color: var(--glow-color);
	font-family: 'SpaceTron';
	text-align: center;
	font-size: 3vh;
	gap: 10vh;
	-webkit-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
		0 0 0.45em var(--glow-color);
	-moz-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
		0 0 0.45em var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.score-line {
	letter-spacing: 0.2em;
	margin: 8vh 0;
	padding: 2vh 3vw;
	border: 0.15em solid var(--glow-color);
	border-radius: 0.45em;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
}

@media (max-width: 980px) {
		.canvas {
		display: flex;
		flex-direction: row;
		width: 50vw;
		height: 50vh;
		box-sizing: border-box;
		justify-content: space-between;
		gap: 8vw;
	}

	.score-header {
		margin: 3vh 15vw;
		color: var(--glow-color);
		font-family: 'SpaceTron';
		text-align: center;
		font-size: 3vh;
		-webkit-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
			0 0 0.45em var(--glow-color);
		-moz-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
			0 0 0.45em var(--glow-color);
		text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	}

	#gameCanvas {
		transform: translateY(5vh);
	}
}
</style>