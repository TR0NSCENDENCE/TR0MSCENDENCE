<template>
	<div class="color_palette">
		<div class="button_line">
			<GlowingButton :text="'green'" @click="changeGlowColor('hsl(120, 100%, 50%)', 'hsl(120, 100%, 7%)', 'sepia(100%) saturate(1000%) hue-rotate(-240deg) contrast(180%) brightness(1.2)', '#00ff00')"/>
			<GlowingButton :text="'red'" @click="changeGlowColor('hsl(0, 100%, 59%)', 'hsl(0, 100%, 7%)', 'sepia(100%) saturate(1000%) hue-rotate(-35deg) contrast(180%) brightness(1.2)', '#ff0000')"/>
		</div>
		<div class="button_line">
			<GlowingButton :text="'yellow'" @click="changeGlowColor('hsl(60, 100%, 50%)', 'hsl(90, 100%, 7%)', 'sepia(100%) saturate(1000%) hue-rotate(35deg) contrast(100%) brightness(1.8)', '#ffff00')"/>
			<GlowingButton :text="'blue'" @click="changeGlowColor('hsl(180, 90%, 50%)', 'hsl(180, 100%, 7%)', 'sepia(100%) saturate(1000%) hue-rotate(-210deg) contrast(120%) brightness(1.8)', '#00ffff')"/>
		</div>
	</div>
</template>

<script setup>
import GlowingButton from '@/components/GlowingButton.vue';

const changeGlowColor = (color, b_color, logo_color, mesh_color) => {
  document.documentElement.style.setProperty('--glow-color', color);
  document.documentElement.style.setProperty('--background-color', b_color);
  document.documentElement.style.setProperty('--logo-filter', logo_color);
  document.documentElement.style.setProperty('--mesh-color', mesh_color);
};

</script>

<style scoped>
.color_palette {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.button_line {
	display: flex;
	gap: 6vh;
	margin: 1vh 0;
}

.button_line:first-of-type {
	margin-bottom: 3vh;
}

.button_line:last-of-type {
	margin-top: 3vh;
}
</style>
