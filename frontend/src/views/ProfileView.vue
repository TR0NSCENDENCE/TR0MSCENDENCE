<template>
	<div>
		<ProfileViewer :pk="userId"/>
	</div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import ProfileViewer from '@components/ProfileViewer.vue';

const route = useRoute();
const userId = route.params.id;
</script>

<style scoped>
#not-exist
{
	display: flex;
	flex-direction: column;
	align-items: center;
}

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
