<template>
	<div class="container">
		<PongGame :config="config" />
	</div>
</template>

<script setup>
import PongGame from '@components/PongGame.vue';
import { config } from '@assets/game_config/pong/solo'
</script>

<style scoped>
.container {
	height: 100%;
	width: 100%;
}
</style>
