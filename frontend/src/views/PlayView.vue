<template>
	<ButtonList :buttons="buttons"/>
</template>

<script setup>
import ButtonList from '@/components/ButtonList.vue';

const buttons = [
	{ text: 'local', dest: 'play/local', needAuth: false},
	{ text: 'multiplayer', dest: 'play/multiplayer', needAuth: true},
	{ text: 'tournament', dest: 'play/tournament', needAuth: true},
];
</script>

<style scoped>
</style>
