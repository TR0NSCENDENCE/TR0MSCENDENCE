<template>
	<ButtonCross :buttons="buttons"/>
</template>

<script setup>
import ButtonCross from '@/components/ButtonCross.vue';

const buttons = [
	{ text:"color", dest:"/settings/settings_color" },
	{ text:"graphics", dest:"/settings/settings_graphics" },
	{ text:"credits", dest:"/settings/credits" },
	{ text:"audio", dest:"/settings/settings_audio" },
];
</script>

<style scoped>
</style>
