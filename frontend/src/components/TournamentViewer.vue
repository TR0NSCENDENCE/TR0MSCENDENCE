<template>
	<div class="tournament-viewer">
		<p>
			{{ new Date(tournamentdata.finished_at).toLocaleString() }}
		</p>
		<div class="tournament-oponants-result">
			<div class="half-matchs">
				<h1>Semi Finals</h1>
				<div class="half-match">
					<UserViewer
						:class="{ user_looser: !isInstanceWinner(tournamentdata.gameinstance_half_1, tournamentdata.gameinstance_half_1.player_one.pk) }"
						:userdata="tournamentdata.gameinstance_half_1.player_one"/>
					<span id="vs">vs</span>
					<UserViewer
						:class="{ user_looser: !isInstanceWinner(tournamentdata.gameinstance_half_1, tournamentdata.gameinstance_half_1.player_two.pk) }"
						:userdata="tournamentdata.gameinstance_half_1.player_two"/>
				</div>
				<div class="half-match">
					<UserViewer
						:class="{ user_looser: !isInstanceWinner(tournamentdata.gameinstance_half_2, tournamentdata.gameinstance_half_2.player_one.pk) }"
						:userdata="tournamentdata.gameinstance_half_2.player_one"/>
					<span id="vs">vs</span>
					<UserViewer
						:class="{ user_looser: !isInstanceWinner(tournamentdata.gameinstance_half_2, tournamentdata.gameinstance_half_2.player_two.pk) }"
						:userdata="tournamentdata.gameinstance_half_2.player_two"/>
				</div>
			</div>
			<div class="final-match-container">
				<h1>Final</h1>
				<div class="final-match">
					<UserViewer
						:class="{ user_looser: !isInstanceWinner(tournamentdata.gameinstance_final, tournamentdata.gameinstance_final.player_one.pk) }"
						:userdata="tournamentdata.gameinstance_final.player_one"/>
					<span id="vs">vs</span>
					<UserViewer
						:class="{ user_looser: !isInstanceWinner(tournamentdata.gameinstance_final, tournamentdata.gameinstance_final.player_two.pk) }"
						:userdata="tournamentdata.gameinstance_final.player_two"/>
				</div>
			</div>
			<div class="final-match-container">
				<h1>WINNER</h1>
				<UserViewer class="final-winner" :pk="tournamentdata.winner_final"/>
			</div>
		</div>
	</div>
</template>

<script setup>
import UserViewer from './UserViewer.vue';

function isInstanceWinner(instance, player) {
	return instance.winner == player;
}

const props = defineProps(['tournamentdata']);
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

.half-matchs, .final-match-container {
	display: flex;
	margin: 2vmin;
	flex-direction: column;
	align-items: center;
	justify-content: left;
	border: 0.15em solid var(--glow-color);
	border-radius: 0.45em;
	letter-spacing: 0.2em;
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.final-winner {
	margin: 2vmin;
}

.user_looser {
	--glow-color: rgb(150, 150, 150);
}

.half-match, .final-match {
	display: flex;
	flex-direction: row;
	align-items: center;
	margin: 1vmin;
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
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}
</style>