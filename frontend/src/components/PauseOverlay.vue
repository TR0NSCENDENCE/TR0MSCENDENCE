<template>
	<div class="overlay">
		<div class="menu">
			<GlowingButton :text="'Resume Game'" @click="resumeGame" />
			<GlowingButton :text="'Quit Game'" :dest="'/'" />
		</div>
	</div>
</template>

<script setup>
import GlowingButton from '@/components/GlowingButton.vue';

const emit = defineEmits(['resume']);

function resumeGame() {
	emit('resume');
}
</script>

<style scoped>
.overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.8);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
}

.menu {
	display: flex;
	flex-direction: column;
	background: black;
	padding: 2vh;
	border-radius: 1vh;
	text-align: center;
	gap: 3vh;
	margin: 1vh 0;
}
</style>