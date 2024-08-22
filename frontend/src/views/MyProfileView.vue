<template>
	<div>
		<div v-if="store.getters.isAuthenticated">
			<ProfileViewer :pk="store.getters.userId"/>
		</div>
		<div v-else class="profile">
			<h1>looks like you're not logged in ...</h1>
		</div>
	</div>
</template>

<script setup>
import ProfileViewer from '@components/ProfileViewer.vue';
import store from '@store';
</script>

<style scoped>
h1 {
	display: flex;
	justify-content: center;
	align-items: center;
	text-align: center;
	margin-top: 30vh;
	letter-spacing: 0.3em;
	font-size: 5vh;
	color: var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}
</style>
