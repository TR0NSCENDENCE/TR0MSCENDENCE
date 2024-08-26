<template>
	<GameOponentsBar
		:player_1="users[0]"
		:player_2="users[1]"
		/>
	<PongGame
		:render_config="config_local"
		@onUpdateRequested="onUpdateRequested"
		ref="game"
		/>
</template>

<script setup>
import { config_local } from '@assets/game/pong/render_config.json'
import GameOponentsBar from '@components/GameOponentsBar.vue';
import PongGame from '@components/PongGame.vue';
import { KEYBOARD } from '@scripts/KeyboardManager';
import { ref } from 'vue'
import store from '@store';

let users = ref([
	{
		score: 0
	},
	{
		score: 0
	}
]);

let players = [
	{
		right: false,
		left: false
	},
	{
		right: false,
		left: false
	}
];

let game = ref(null);

const updatePlayer = (id, left, right) => {
	const dir = {
		right: KEYBOARD.isKeyDown(right),
		left: KEYBOARD.isKeyDown(left)
	};

	if (dir === players[id])
		return ;
	players[id] = dir;
	const direction = (dir.left ? -1 : 0) + (dir.right ? 1 : 0);
	store.commit('pong/set_player_direction', {id, direction});
}

const onUpdateRequested = () => {
	updatePlayer(1, 's', 'w');
	updatePlayer(0, 'ArrowDown', 'ArrowUp');
	const scores = game.value.getScores();
	users.value[0].score = scores[0];
	users.value[1].score = scores[1];
}
</script>

<style scoped>
</style>
