<template>
	<div id="activation-view">
		<div v-if="activated">
			<h1>Your account was successfully activated !</h1>
			<GlowingButton style="margin-bottom: 2vmin;" :text="'login'" :dest="'/login'"/>
			<GlowingButton :text="'go back home'" :dest="'/'"/>
		</div>
		<div v-else-if="is_error">
			<h1>An error occured !</h1>
			<GlowingButton :text="'go back home'" :dest="'/'"/>
		</div>
	</div>
</template>

<script setup>
import GlowingButton from '@components/GlowingButton.vue';
import router from '@router/index';
import { axiosInstance } from '@utils/api';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const UUID = useRoute().params.uuid;
const activated = ref(false);
const is_error = ref(false);

onMounted(() => {
	axiosInstance.get(`/activation/${UUID}/`).then(
		(response) => activated.value = true,
	).catch(
		(error) => is_error.value = true
	);
})
</script>

<style scoped>
#activation-view {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

#activation-view > div {
	display: flex;
	flex-direction: column;
	align-items: center;
	color: var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

h1 {
	font-size: 4vmin;
	margin-bottom: 10vmin;
	text-align: center;
}
</style>
