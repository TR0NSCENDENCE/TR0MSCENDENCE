<template>
    <ButtonList :buttons="buttons"/>
</template>

<script setup>
import ButtonList from '@/components/ButtonList.vue';

const buttons = [
    { text: 'solo', dest: 'minigame/solo'},
    { text: '1 v 1', dest: 'minigame/1v1'},
    { text: 'game history', dest: 'minigame/game_history'},
];
</script>

<style scoped>
</style>