<template>
	<div class="leaderboard">
		<table>
			<thead>
				<tr>
					<th>Rank</th>
					<th>Name</th>
					<th>Winrate</th>
					<th>Winned</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(player) in players" :key="player.id">
					<td>#{{ player.rank }}</td>
					<td>
							{{ player.username }}
					</td>
					<td>{{ Math.round(player.win_rate) }}%</td>
					<td>{{ player.num_wins }}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
import { axiosInstance } from '@utils/api';
import { onMounted, ref } from 'vue';

const players = ref([]);

const next = ref(null);
const prev = ref(null);
const curpage = ref(0);
const totalpage = ref(0);

function _updatePlayerList(url) {
	axiosInstance.get(url).then(
		(response) => {
			curpage.value = new URL(response.request.responseURL).searchParams.get('page') || 1
			totalpage.value = Math.ceil(response.data.count / 5);
			next.value = response.data.next;
			prev.value = response.data.previous
			players.value = response.data.results;
		}
	);
}

function updatePlayerList() {
	_updatePlayerList(`/leaderboard/`);
}

onMounted(updatePlayerList);

</script>

<style scoped>
.leaderboard {
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
