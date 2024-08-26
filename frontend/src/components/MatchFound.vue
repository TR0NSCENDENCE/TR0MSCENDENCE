<template>
	<div id="match_found">
		<h1 id="match_found_label">match found :</h1>
		<UserViewer :userdata="player1"/>
		<div class="versus">
			<div class="letter" id="letter_V">v</div>
			<div class="letter" id="letter_S">s</div>
		</div>
		<UserViewer :userdata="player2"/>
	</div>
</template>

<script setup>
import UserViewer from './UserViewer.vue';

const props = defineProps([ 'player1', 'player2' ]);
</script>

<style scoped>
#match_found_p1, #match_found_p2 {

	/* animation: fadeIn 2s forwards; */
}

#match_found_label {
	font-size: 5vh;
}

#match_found {
	color: var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	letter-spacing: 0.1em;
	font-weight: bold;
	display: flex;
	flex-direction: column;
	align-items: center;
}

#letter_V {
	margin-top: 100%;
	font-size: 5vh;
	animation: moveToCenterV 2s forwards;
}

#letter_S {
	margin-bottom: 100%;
	font-size: 5vh;
	animation: moveToCenterS 2s forwards;
}

@keyframes moveToCenterV {
	from {
		transform: translate(-50px, 0);
		opacity: 0;
	}
	to {
		transform: translate(0, 0);
		opacity: 1;
	}
}

@keyframes moveToCenterS {
	from {
		transform: translate(50px, 0);
		opacity: 0;
	}
	to {
		transform: translate(0, 0);
		opacity: 1;
	}
}

@keyframes fadeIn {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}
</style>
