<template>
	<h1>looks like you got lost ...</h1>
	<div id="unknown_page">
		<GlowingButton :text="'go back home'" :dest="'/'"/>
	</div>
</template>

<script setup>
import GlowingButton from '@components/GlowingButton.vue';
</script>

<style scoped>
#unknown_page {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	width: 100%;
}

h1 {
	margin-top: 10vh;
	font-size: 5vh;
	text-align: center;
	color: var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	letter-spacing: 0.5em;
}
</style>
