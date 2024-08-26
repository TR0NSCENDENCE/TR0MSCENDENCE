<template>
	<PongGame
		@onUpdateRequested="onUpdateRequested"
		/>
</template>

<script setup>
import PongGame from '@components/PongGame.vue';
import { Direction } from '@scripts/games/pong/utils';
import { KEYBOARD } from '@scripts/KeyboardManager';
import store from '@store';

let player_one_dir = Direction.NONE;

// TODO: IA

const onUpdateRequested = () => {
	const right = KEYBOARD.isKeyDown('ArrowRight') || KEYBOARD.isKeyDown('d');
	const left = KEYBOARD.isKeyDown('ArrowLeft') || KEYBOARD.isKeyDown('a');
	const direction = (left ? -1 : 0) + (right ? 1 : 0);
	
	if (direction === player_one_dir)
		return ;
	player_one_dir = direction;
	store.commit('pong/set_player_direction', {id: 0, direction: direction});
}
</script>

<style scoped>
</style>
