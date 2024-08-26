<template>
	<div class="color_palette">
		<div class="button_line">
			<GlowingButton text="green" @click="store.commit('changeSelectedTheme', 'green')" />
			<GlowingButton text="red" @click="store.commit('changeSelectedTheme', 'red')" />
		</div>
		<div class="button_line">
			<GlowingButton text="yellow" @click="store.commit('changeSelectedTheme', 'yellow')" />
			<GlowingButton text="blue" @click="store.commit('changeSelectedTheme', 'blue')" />
		</div>
	</div>
</template>

<script setup>
import GlowingButton from '@/components/GlowingButton.vue';
import store from '@store';
</script>

<style scoped>
.color_palette {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.button_line {
	display: flex;
	gap: 6vh;
	margin: 1vh 0;
}

.button_line:first-of-type {
	margin-bottom: 3vh;
}

.button_line:last-of-type {
	margin-top: 3vh;
}
</style>
