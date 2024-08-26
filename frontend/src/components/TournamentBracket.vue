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
		<div class="matches-right">
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
</template>

<script setup>

import { ref } from 'vue';
import UserViewer from './UserViewer.vue';

const props = defineProps(['tournamentdata']);
</script>

<style scoped>
.bracket {
	display: flex;
	justify-content: space-between;
	align-items: center;
	width: 70vw;
	color: var(--glow-color);
	font-size: 2vmin;
}

.matches-left {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 10vh;
	/* Réduit l'espacement entre les demi-finales */
	position: relative;
}

.match {
	display: flex;
	flex-direction: column;
	align-items: center;
	width: 100%;
}

.match > div {
	width: 100%;
}

.final {
	display: flex;
	flex-direction: column;
	align-items: center;
	position: relative;
}

.winner {
	display: flex;
}

.vs {
	margin: 1vh 0;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

</style>
