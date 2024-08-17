<template>
	<Suspense>
		<ProfileViewer :data="data"/>
		<template #fallback>
		</template>
	</Suspense>
</template>

<script setup>
import utils from '@utils'
import { ref, onMounted } from 'vue'
import ProfileViewer from '@components/ProfileViewer.vue';
import store from '@store';

const data = ref({
	user: {},
	stats: {}
});

async function getMyProfile() { //modifier et mettre un getter pour le profile cible
	return new Promise((resolve, reject) => {
		utils.makeAuthApiQuery('/me', 'get', {}, //changer /me par ??
			(result) => {
				data.value.user = result.data.user;
			},
			(error) => {
				console.log(error);
			}
		);
	})
}

onMounted(async () => {
	if (store.getters.isAuthenticated)
		await getMyProfile(); //modif ici aussi
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
