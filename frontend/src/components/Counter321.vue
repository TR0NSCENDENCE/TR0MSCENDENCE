<template>
	<div class="counter_container">
		<div class="counter" :class="{ 'counter_active': is_active }"></div>
	</div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const emits = defineEmits(['finished'])

const is_active = ref(false);
let timer = undefined;

function start() {
	is_active.value = true;
	setTimeout(
		() => {
			emits('finished');
			is_active.value = false;
			timer = undefined;
		},
		3000
	);
}

function stop() {
	is_active.value = false;
	if (timer) {
		clearTimeout(timer);
		timer = undefined;
	}
}

onUnmounted(() => {
	stop()
})

defineExpose({
	start: start,
	stop: stop
});

</script>

<style scoped>
.counter_container {
	background-color: #000000;
	margin: 0 auto;
	width: 50px;
	height: 50px;
}

.counter {
	position: relative;
	background-color: var(--glow-color);
	margin: 0 auto;
	width: 40%;
	height: 60%;
	border-radius: 30px;
	display: none;
}

.counter_active {
	display: block;
}

.counter_active:before,
.counter_active:after {
	content: " ";
	position: absolute;
	background-color: #000000;
	width: 50%;
	height: 33.3333334%;
	animation-duration: 3s;
	animation-timing-function: ease-in-out;
	animation-iteration-count: 1;
	animation-direction: normal;
	animation-fill-mode: forwards;
}

.counter_active:before {
	top: 16.6666667%;
	left: 25%;
	animation-name: contagem1;
}

.counter_active:after {
	top: 58.3333333%;
	left: 25%;
	animation-name: contagem2;
}

@keyframes contagem1 {

	0%,
	30%,
	35%,
	65% {
		top: 16.6666667%;
		left: 0%;
		width: 75%;
		height: 25%;
	}

	70%,
	100% {
		top: 0%;
		left: 0%;
		width: 75%;
		height: 50%;
	}
}

@keyframes contagem2 {

	0%,
	30% {
		top: 58.3333333%;
		left: 0%;
		width: 75%;
		height: 25%;
	}

	35%,
	65% {
		top: 58.3333333%;
		left: 25%;
		width: 75%;
		height: 25%;
	}

	70%,
	100% {
		top: 50%;
		left: 0%;
		width: 75%;
		height: 50%;
	}
}
</style>
