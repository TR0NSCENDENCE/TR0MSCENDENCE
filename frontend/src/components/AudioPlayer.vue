<template>
	<audio ref="audioElement" class="audio-player" controls loop>
		<source :src="currentTrack" type="audio/mpeg" />
	</audio>
</template>

<script setup>
import { computed, watch, ref } from 'vue';
import store from '@store';

const currentTrack = computed(() => store.getters['audio/currentTrack']);
const volume = computed(() => store.getters['audio/volume']);
const isPlaying = computed(() => store.getters['audio/isPlaying']);

const audioElement = ref(null);

watch(currentTrack, (newVal) => {
	if (audioElement.value) {
		audioElement.value.src = newVal;
		if (isPlaying.value) {
			audioElement.value.play();
		}
	}
});

watch(isPlaying, (newVal) => {
	if (audioElement.value) {
		if (newVal) {
			audioElement.value.play();
		} else {
			audioElement.value.pause();
		}
	}
});

watch(volume, (newVolume) => {
	if (audioElement.value) {
		audioElement.value.volume = newVolume;
	}
});
</script>

<style scoped>
.audio-player {
	margin: 0 1em;
	border-radius: 10px;
	width: 40%;
	scale: 1;
	opacity: 70%;
}

/* Webkit-based browsers (Chrome, Safari, Edge) */
.audio-player::-webkit-media-controls-panel {
	background-color: var(--glow-color);
	border-radius: 10px;
}

/* Play/Pause buttons */
.audio-player::-webkit-media-controls-play-button,
.audio-player::-webkit-media-controls-pause-button {
	color: black;
}

/* timers */
.audio-player::-webkit-media-controls-current-time-display,
.audio-player::-webkit-media-controls-time-remaining-display {
	color: black;
}

/* Progress bar */
.audio-player::-webkit-media-controls-seek-bar {
	background-color: var(--glow-color);
}

.audio-player::-webkit-media-controls-volume-slider {
	background-color: var(--glow-color);
	color: black;
}
</style>
