<template>
	<div id="root">
		<header>
			<HeaderBar />
		</header>
		<main>
			<RouterView />
		</main>
		<footer>
			<FooterBar />
		</footer>
	</div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import FooterBar from '@components/FooterBar.vue';
import HeaderBar from '@components/HeaderBar.vue';
</script>

<style>
:root {
	--glow-color: hsl(0, 100%, 59%);
	--background-color: hsl(0, 100%, 7%);
	--logo-filter: sepia(100%) saturate(1000%) hue-rotate(-35deg) contrast(180%) brightness(1.2);
	--mesh-color: #ff0000;
}

@font-face {
	font-family: 'SpaceTron';
	src: url('/fonts/spacetron-51nwz.otf') format('opentype');
}

@font-face {
	font-family: 'Orbitron';
	src: url('/fonts/Orbitron-VariableFont_wght.ttf') format('truetype');
}

#header {
	display: flex;
	align-items: center;
}

#root {
	font-family: "SpaceTron", sans-serif;
	font-size: 1em;
	background-color: black;
	display: flex;
	flex-direction: column;
	min-height: 100vh;
	margin: 0;
}

main {
	display: grid;
	flex: 1;
}

header,
footer {
	background-color: black;
	margin: 1vh;
}
</style>
