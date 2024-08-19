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
