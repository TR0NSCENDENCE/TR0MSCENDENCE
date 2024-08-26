<template>
	<PongGame
		@onUpdateRequested="onUpdateRequested"
		/>
</template>

<script setup>
import PongGame from '@components/PongGame.vue';
import { KEYBOARD } from '@scripts/KeyboardManager';
import store from '@store';

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
	updatePlayer(0, 'a', 'd');
	updatePlayer(1, 'ArrowLeft', 'ArrowRight');
}
</script>

<style scoped>
</style>
