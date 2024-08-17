<template>
	<Suspense>
		<ProfileViewer v-if="exist" :data="data"/>
		<div id="not-exist" v-else>
			<h1>User requested does not exist.</h1>
			<GlowingButton class="go-back-button small-button" :text="'go back'" :dest="'/'"/>
		</div>
		<template #fallback>
		</template>
	</Suspense>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router';
import utils from '@utils'
import GlowingButton from '@components/GlowingButton.vue';
import ProfileViewer from '@components/ProfileViewer.vue';
import store from '@store';

const route = useRoute();

const userId = route.params.id;
const exist = ref(true);

const data = ref({});

async function getMyProfile() {
	return new Promise((resolve, reject) => {
		utils.makeAuthApiQuery('/user/' + userId + '/', 'GET', {},
			(result) => data.value = result.data,
			(error) => {
				console.log(error);
				exist.value = false;
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
