<template>
	<div class="bracket">
		<!-- Colonne de gauche pour les demi-finales -->
		<div class="matches-left">
			<div class="match">
				<UserViewer :userdata="tournamentdata.gameinstance_half_1.player_one"/>
				<span class="vs">VS</span>
				<UserViewer :userdata="tournamentdata.gameinstance_half_1.player_two"/>
			</div>
			<div class="match">
				<UserViewer :userdata="tournamentdata.gameinstance_half_2.player_one"/>
				<span class="vs">VS</span>
				<UserViewer :userdata="tournamentdata.gameinstance_half_2.player_two"/>
			</div>
		</div>
		<!-- Section pour la finale et le gagnant -->
		<div class="final-and-winner">
			<div class="final">
				<div class="match" v-if="tournamentdata.winner_half_1 || tournamentdata.winner_half_2">
					<UserViewer :pk="tournamentdata.winner_half_1" v-if="tournamentdata.winner_half_1"/>
					<span class="vs">VS</span>
					<UserViewer :pk="tournamentdata.winner_half_2" v-if="tournamentdata.winner_half_2"/>
				</div>
			</div>
			<div class="winner" v-if="tournamentdata.winner_final">
				<UserViewer :pk="tournamentdata.winner_final"/>
			</div>
		</div>
	</div>
</template>

<script setup>

import { ref } from 'vue';
import UserViewer from './UserViewer.vue';

const props = defineProps(['tournamentdata']);
</script>

<style scoped>
.bracket {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 2vh;
	/* Espacement global entre les colonnes */
	align-items: center;
	justify-content: center;
	color: var(--glow-color);
	--size-factor: (0.00188323 * 70vw);
	font-size: calc(8 * var(--size-factor));
	transform: translateY(10vh) translateX(-6.1vw);
	position: relative;
	/* Nécessaire pour les lignes absolues */
}

.matches-left {
	display: flex;
	flex-direction: column;
	gap: 10vh;
	/* Réduit l'espacement entre les demi-finales */
	position: relative;
}

.match {
	display: flex;
	flex-direction: column;
	align-items: center;
	position: relative;
}

.final-and-winner {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 10vh;
	/* Réduit l'espacement entre la finale et le gagnant */
	position: relative;
}

.final {
	display: flex;
	flex-direction: column;
	align-items: center;
	position: relative;
}

.winner {
	display: flex;
	justify-content: center;
	align-items: center;
	transform: translateX(6.3vw);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	position: relative;
}

.team {
	border: 2px solid var(--glow-color);
	padding: 1vh 2vh;
	border-radius: 0.5vh;
	width: 30vh;
	text-align: center;
	box-sizing: border-box;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	animation: border-flicker 7s linear infinite;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	white-space: nowrap;
	/* Évite les retours à la ligne */
	overflow: hidden;
	/* Cache le texte qui dépasse */
	text-overflow: ellipsis;
}

.vs {
	margin: 1vh 0;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.final .team {
	border: 2px solid var(--glow-color);
	padding: 1vh 2vh;
	border-radius: 0.5vh;
	width: 30vh;
}

.winner .team {
	border: 2px solid var(--glow-color);
	padding: 1vh 2vh;
	border-radius: 5px;
	width: 30vh;
	font-weight: bold;
}
</style>
