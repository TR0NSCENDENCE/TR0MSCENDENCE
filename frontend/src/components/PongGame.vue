<template>
	<div class="pong_game">
		<div class="pong_game_container">
			<Counter321 ref="counter"/>
			<div id="canvas_container" ref="canvas_container">
				<canvas
					id="pong_game_canvas"
					ref="pong_game_canvas"
					>
				</canvas>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Counter321 from '@components/Counter321.vue';
import PongController from '@scripts/games/pong/controller';
import PongRenderer from '@scripts/games/pong/renderer';
import store from '@store';
import PongModel from '@scripts/games/pong/model';
import { Direction } from '@scripts/games/pong/utils';

const emits = defineEmits([
	'onUpdateRequested'
]);
const props = defineProps([
	'render_config',
	'enable_simulation'
])

const game = {
	/** @type {PongModel} */ model: undefined,
	/** @type {PongController} */ controller: undefined,
	/** @type {PongRenderer} */ renderer: undefined
};

const counter = ref(null);
const pong_game_canvas = ref(null);
const canvas_container = ref(null);

let animation_frame_handle = undefined;

const animate = () => {
	game.controller.step();
	animation_frame_handle = requestAnimationFrame(animate);
}

const setupController = () => {
	const controller = game.controller;

	controller.onUpdateRequested = () => emits('onUpdateRequested');
	controller.onCountdownStart = () => counter.value.start();
	controller.onCountdownStop = () => counter.value.stop();
	controller.onPlayerOneInputRequested = () => Direction.None;
	controller.onPlayerTwoInputRequested = () => Direction.None;
}

onMounted(() => {
	game.renderer = new PongRenderer(
		props.render_config,
		pong_game_canvas,
		canvas_container,
		store.getters.theme
	);
	game.model = new PongModel();
	game.controller = new PongController(
		game.model,
		game.renderer,
		props.enable_simulation ?? true
	);
	setupController();
	animation_frame_handle = requestAnimationFrame(animate);
});

onUnmounted(() => {
	if (animation_frame_handle)
		cancelAnimationFrame(animation_frame_handle);
	if (game.renderer)
		game.renderer.cleanup();
});

defineExpose({
	onCountdownStart: () => counter.value.start(),
	onCountdownStop: () => counter.value.stop(),
	getScores: () => game.model.getScores(),
	forceUpdate: (data) => game.model.forceUpdate(data)
});

</script>

<style scoped>
@font-face {
	font-family: 'SpaceTron';
	src: url('/fonts/spacetron-51nwz.otf') format('opentype');
	font-weight: normal;
	font-style: normal;
}

#canvas_container {
	width: 100vmin;
	/* (100/16) * 9 */
	height: 56.25vmin;
	border: solid 0.25em var(--glow-color);
	border-radius: 0.45em;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
}

.pong_game {
	height: 100%;
	width: 100%;
}

.pong_game_header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 10px;
	color: var(--glow-color);
	height: 10%;
	width: 100%;
	font-family: 'SpaceTron', sans-serif;
}

.pong_game_container {
	display: flex;
	align-items: center;
	flex-direction: column;
}

.pong_game_canvas_container {
	display: flex;
	align-items: center;
	justify-content: center;
}

.pong_game_player,
.pong_game_score_header {
	flex: 1;
	text-align: center;
	padding: 10px;
}

.pong_game_commands {
	font-size: 0.5em;
}
</style>
