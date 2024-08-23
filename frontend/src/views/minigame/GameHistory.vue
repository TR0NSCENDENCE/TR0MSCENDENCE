<template>
	<div class="leaderboard_solo ">
        <h1 class="solo"> solo </h1>
		<table>
			<thead>
				<tr>
					<th>best score</th>
					<th>best time</th>
					<th>games played</th>
					<th>winrate</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(solo) in solo" :key="solo.id">
					<td>{{ solo.best_score }}</td>
					<td>{{ solo.best_time }}</td>
					<td>{{ solo.game_played }} </td>
					<td>{{ solo.winrate }}</td>
				</tr>
			</tbody>
		</table>
	</div>
    <div class="leaderboard_1v1">
        <h1 class="versus"> 1v1 </h1>
		<table>
			<thead>
				<tr>
					<th>best score</th>
					<th>best time</th>
					<th>games played</th>
					<th>winrate</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(versus) in versus" :key="versus.id">
					<td>{{ versus.best_score }}</td>
					<td>{{ versus.best_time }}</td>
					<td>{{ versus.game_played }} </td>
					<td>{{ versus.winrate }}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
// Fonction pour récupérer les scores
function getScores() {
    return (JSON.parse(localStorage.getItem('pacman_scores')) || []);
}

// Fonction pour récupérer les scores
function getTimes() {
    return (JSON.parse(localStorage.getItem('pacman_times')) || []);
}


const solo = [
	{ best_score: getScores(), best_time: getTimes(), game_played: 92, winrate: 1500 },
];

const versus = [
	{ best_score: 1, best_time: 'Alice', game_played: 92, winrate: 1500 },
];
</script>

<!-- <template>
	<div class="leaderboard_solo">
	  <h1 class="solo">Solo</h1>
	  <table>
		<thead>
		  <tr>
			<th>Best Score</th>
			<th>Best Time</th>
			<th>Games Played</th>
			<th>Winrate</th>
		  </tr>
		</thead>
		<tbody>
		  <tr v-for="(entry) in soloData" :key="entry.id">
			<td>{{ entry.best_score }}</td>
			<td>{{ entry.best_time }}</td>
			<td>{{ entry.game_played }}</td>
			<td>{{ entry.winrate }}</td>
		  </tr>
		</tbody>
	  </table>
	</div>
	<div class="leaderboard_1v1">
	  <h1 class="versus">1v1</h1>
	  <table>
		<thead>
		  <tr>
			<th>Best Score</th>
			<th>Best Time</th>
			<th>Games Played</th>
			<th>Winrate</th>
		  </tr>
		</thead>
		<tbody>
		  <tr v-for="(entry) in versusData" :key="entry.id">
			<td>{{ entry.best_score }}</td>
			<td>{{ entry.best_time }}</td>
			<td>{{ entry.game_played }}</td>
			<td>{{ entry.winrate }}</td>
		  </tr>
		</tbody>
	  </table>
	</div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const soloData = ref([]);
  const versusData = ref([]);
  
  onMounted(async () => {
	try {
	  const response = await fetch('@assets/data/pacman_data.json');
	  const data = await response.json();
	  soloData.value = data.solo;
	  versusData.value = data.versus;
	} catch (error) {
	  console.error('Error fetching data:', error);
	}
  });
  </script>
   -->

<style scoped>
.leaderboard_solo, .leaderboard_1v1 {
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
