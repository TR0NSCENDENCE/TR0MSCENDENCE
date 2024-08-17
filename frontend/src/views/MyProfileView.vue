<template>
	<Suspense v-if="store.getters.isAuthenticated">
		<ProfileViewer :data="data"/>
		<template #fallback>
		</template>
	</Suspense>
	<div v-else class="profile">
		<h1>looks like you're not logged in ...</h1>
	</div>
</template>

<script setup>
import utils from '@utils'
import { ref, onMounted } from 'vue'
import ProfileViewer from '@components/ProfileViewer.vue';
import store from '@store';

const data = ref({});

async function getMyProfile() {
	return new Promise((resolve, reject) => {
		utils.makeAuthApiQuery('/me/', 'get', {},
			(result) => {
				data.value = result.data;
			},
			(error) => {
				console.log(error);
			}
		);
	})
}

onMounted(async () => {
	if (store.getters.isAuthenticated)
		await getMyProfile();
});
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
