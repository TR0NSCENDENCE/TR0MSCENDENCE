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
import PongLogic from '@scripts/games/pong/logic';
import PongRenderer from '@scripts/games/pong/renderer';

const emits = defineEmits(['onUpdateRequested']);

const game = {
	logic: new PongLogic(),
	renderer: undefined
};

const counter = ref(null);
const pong_game_canvas = ref(null);
const canvas_container = ref(null);

let animation_frame_handle = undefined;

function animate() {
	emits('onUpdateRequested')
	game.logic.step();
	game.renderer.render();
	animation_frame_handle = requestAnimationFrame(animate);
}

onMounted(() => {
	game.renderer = new PongRenderer(
		pong_game_canvas,
		canvas_container,
		document.documentElement.style.getPropertyValue('--glow-color')
	);
	game.logic.setCallbackUpdateFinished(game.renderer.updateState);
	animation_frame_handle = requestAnimationFrame(animate);
});

onUnmounted(() => {
	if (animation_frame_handle)
		cancelAnimationFrame(animation_frame_handle);
	if (game.renderer)
		game.renderer.cleanup();
})

defineExpose({
	setCounterActive: (active) => {
		if (active)
			counter.value.start();
		else
			counter.value.stop();
	},
	setters: {
		ball: game.logic.setBall,
		paddle_1: game.logic.setPaddle1,
		paddle_2: game.logic.setPaddle2
	}
})

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
