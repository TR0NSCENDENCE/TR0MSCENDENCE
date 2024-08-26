<template>
	<div class="pong_game_header">
		<h1>player 1 |</h1>
		<UserViewer v-if="player_1.user" :userdata="player_1.user"/>
		<h1 class="pong_game_score_header">
			 {{ player_1.score }} - {{ player_2.score }}
		</h1>
		<h1>| player 2</h1>
		<UserViewer v-if="player_2.user" :userdata="player_2.user"/>
	</div>
</template>

<script setup>
import UserViewer from './UserViewer.vue';

const props = defineProps(['player_1', 'player_2']);
</script>

<style scoped>
.pong_game_header {
	color: var(--glow-color);
	--size-factor: (0.00188323 * 70vw);
	font-size: calc(8 * var(--size-factor));
	display: flex;
	align-items: center;
	justify-content: center;
}
.pong_game_header > h1 {
	margin: 10px;
}
</style>
