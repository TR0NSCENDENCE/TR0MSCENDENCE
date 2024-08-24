<template>
	<div class="tournament-viewer">
		<p>
			{{ new Date(data.finished_at).toLocaleString() }}
		</p>
		<div class="match-oponants-result">
			<UserViewer
				:class="{ user_looser: !isInstanceWinner(data, data.player_one.pk) }"
				:userdata="data.player_one"/>
			<span id="vs">vs</span>
			<UserViewer
				:class="{ user_looser: !isInstanceWinner(data, data.player_two.pk) }"
				:userdata="data.player_two"/>
			<p class="score"><span class="score-number">{{ data.player_one_score }}</span> - <span class="score-number">{{ data.player_two_score }}</span></p>
		</div>
	</div>
</template>

<script setup>
import UserViewer from './UserViewer.vue';

function isInstanceWinner(instance, player) {
	return instance.winner == player;
}

const props = defineProps(['data']);
</script>

<style scoped>
#vs {
	font-size: 2em;
	margin-left: 2vw;
	margin-right: 2vw;
}

.score {
	margin-left: 2vw;
	font-size: 2em;
	white-space: nowrap;
}

.user_looser {
	--glow-color: rgb(150, 150, 150);
}

.match-oponants-result {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
}

.tournament-viewer {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 0;
	text-decoration: none;
	color: var(--glow-color);
	border: 0.15em solid var(--glow-color);
	border-radius: 0.45em;
	padding: 1vh 2.5vh;
	letter-spacing: 0.2em;
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	animation: border-flicker 7s linear infinite;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}
</style>