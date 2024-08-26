<template>
    <div class="overlay">
        <div class="lose_text">
            <h1>game over :/</h1>
            <h2>Score: {{ score }}</h2>
            <h2>time: {{ time }}</h2>
        </div>
        <div class="menu">
            <GlowingButton :text="'go back home'" :dest="'/'" />
        </div>
    </div>
</template>

<script setup>
import GlowingButton from '@/components/GlowingButton.vue';
import { defineProps } from 'vue';

const props = defineProps({
    score: {
        type: Number,
        required: true
    },
    time: {
        type: String,
        required: true
    }
});
</script>


<style scoped>
.overlay {
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    --size-factor: (0.00188323 * 70vw);
    font-size: calc(8 * var(--size-factor));
}

h1 {
    font-size: 3em;
}

.lose_text {
    font-family: 'SpaceTron', sans-serif;
    color: var(--glow-color);
    border: solid var(--glow-color) 0.2em;
    border-radius: 0.45em;
    padding: 4vh 3vw;
    -webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
        0px 0px 0.5em 0px var(--glow-color);
    -moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
        0px 0px 0.5em 0px var(--glow-color);
    box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
        0px 0px 0.5em 0px var(--glow-color);
    -webkit-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
        0 0 0.45em var(--glow-color);
    -moz-text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3),
        0 0 0.45em var(--glow-color);
    text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.menu {
    display: flex;
    flex-direction: column;
    background: black;
    padding: 2vh;
    border-radius: 1vh;
    text-align: center;
    gap: 3vh;
    margin: 1vh 0;
}
</style>