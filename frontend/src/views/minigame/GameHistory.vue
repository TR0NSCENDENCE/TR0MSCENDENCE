<template>
	<div class="history">
		<h1 class="history"></h1>
		<table>
			<thead>
				<tr>
					<th>score</th>
					<th>time</th>
					<th>mode</th>
					<th>status</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(entry, index) in history" :key="index">
					<td>{{ entry.score }}</td>
					<td>{{ entry.time }}</td>
					<td>{{ entry.mode }}</td>
					<td>{{ entry.status }}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
import store from '@store';
import { axiosInstance } from '@utils/api';
import { onMounted, ref } from 'vue';

const history = ref([]);

async function _getLocalStats() {
	const jsonData = localStorage.getItem('stats');
	const statsArray = JSON.parse(jsonData) || [];

	const lastFiveGames = statsArray.slice(-5).reverse();

	history.value = lastFiveGames.map(history => ({
		score: history.score,
		time: history.time,
		mode: history.mode,
		status: history.status,
	}));
}

async function _getUserStats() {
	try {
		const response = await axiosInstance.get('/me/pacman-data/');

		const statsArray = response.data.pacman_data || [];
		const lastFiveGames = statsArray.slice(-5).reverse();
	
		history.value = lastFiveGames.map(history => ({
			score: history.score,
			time: history.time,
			mode: history.mode,
			status: history.status,
		}));
	} catch (e) {
		console.log(e);
	}

}

async function getStats() {
	try {
		if (!store.getters.isAuthenticated)
			await _getLocalStats();
		else
			await _getUserStats();
	} catch (e) {
		console.log(e);
	}
}

onMounted(getStats);

</script>

<style scoped>
.history {
	margin: 2vh 7vh 2vh 7vh;
	text-align: center;
	color: var(--glow-color);
	font-family: "SpaceTron", sans-serif;
	--size-factor: (0.00188323 * 70vw);
	font-size: calc(12 * var(--size-factor));
}

.link {
	text-decoration: none;
	color: var(--glow-color);
}

.link:hover {
	opacity: 50%;
	text-shadow: none;
	animation: none;
}

.solo, .versus {
	-webkit-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
		0 0 0.45em var(--glow-color);
	-moz-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
		0 0 0.45em var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

table {
	height: auto;
	width: 100%;
	overflow: hidden;
	font-family: "SpaceTron", sans-serif;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
}


th,
td {
	background-color: var(--background-color);
	padding: 10px;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
}

th {
	font-weight: bolder;
	font-size: larger;
}

tbody tr:nth-child(even) {
	background-color: black;
}

tbody tr:nth-child(odd) {
	background-color: black;
}
</style>
