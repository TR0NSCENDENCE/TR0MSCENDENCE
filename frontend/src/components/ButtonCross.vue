<template>
	<div class="button_cross">
		<GlowingButton
			v-if="buttons.length > 0"
			:text="buttons[0].text"
			:dest="buttons[0].dest"
			class="top-button"
		/>
		<div class="middle-row">
			<GlowingButton
				v-if="buttons.length > 1"
				:text="buttons[1].text"
				:dest="buttons[1].dest"
				class="left-button"
			/>
			<div class="middle-space"></div>
			<GlowingButton
				v-if="buttons.length > 2"
				:text="buttons[2].text"
				:dest="buttons[2].dest"
				class="right-button"
			/>
		</div>
		<GlowingButton
			v-if="buttons.length > 3"
			:text="buttons[3].text"
			:dest="buttons[3].dest"
			class="bottom-button"
		/>
	</div>
</template>

<script setup>
import GlowingButton from '@components/GlowingButton.vue';

const props = defineProps(['buttons']);
</script>

<style scoped>
.button_cross {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 70vh;
	width: 70vw;
	position: relative;
	padding: 2vw;
	box-sizing: border-box;
}

.middle-row {
	display: flex;
	justify-content: space-between;
	width: 50%;
	max-width: 20vw;
}

.middle-space {
	flex: 1;
}

.top-button, .bottom-button {
	position: absolute;
	left: 50vw;
	transform: translateX(-50%);
	width: 40%;
	max-width: 15vw;
}

.top-button {
	top: 10%;
}

.bottom-button {
	bottom: 10%;
}

.left-button, .right-button {
	flex: 1;
	margin: 0 50%;
	width: 40%;
	max-width: 25vw;
}

.left-button {
	margin-left: 0;
}

.right-button {
	margin-right: 0;
}
</style>
