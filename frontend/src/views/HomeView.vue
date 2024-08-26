<template>
	<ButtonList :buttons="buttons"/>
</template>

<script setup>
import ButtonList from '@components/ButtonList.vue';

const buttons = [
	{ text: 'play', dest: 'play', needAuth: false },
	{ text: 'minigame', dest: 'minigame', needAuth: false },
	{ text: 'leaderboard', dest: 'leaderboard', needAuth: false },
	{ text: 'search profile', dest: 'searchprofile', needAuth: false },
	{ text: 'friends', dest: 'friends', needAuth: true },
	{ text: 'settings', dest: 'settings', needAuth: false },
];
</script>

<style scoped>
</style>
