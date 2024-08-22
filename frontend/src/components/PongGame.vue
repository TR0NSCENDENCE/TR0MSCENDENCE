<template>
	<div class="pong_game">
		<div class="pong_game_container">
			<Counter321 ref="counter"/>
			<canvas
				ref="pong_game_canvas"
				style="width: 90%; height:100%;"
				>
			</canvas>
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

function animate() {
	emits('onUpdateRequested')
	game.logic.step();
	game.renderer.render();
	requestAnimationFrame(animate);
}

onMounted(() => {
	const need_resize = () => {
		const canvas = pong_game_canvas.value;
		if (!canvas) return (false);
		const width = pong_game_canvas.value.clientWidth;
		const height = pong_game_canvas.value.clientHeight;
		return (pong_game_canvas.value.width !== width || pong_game_canvas.value.height !== height);
	};

	const get_dims = () => {
		const canvas = pong_game_canvas.value;
		if (!canvas) return ;
		const width = canvas.clientWidth;
		const height = canvas.clientHeight;

		return ({width, height});
	}

	game.renderer = new PongRenderer(
		pong_game_canvas.value,
		0xff0000,
		{
			need_resize,
			get_dims
		}
	);
	game.logic.setCallbackUpdateFinished(game.renderer.updateState);
	requestAnimationFrame(animate);
});

onUnmounted(() => {
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
	height: 90%;
	width: 100%;
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
