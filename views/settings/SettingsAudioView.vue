<template>
	<div id="settings_audio">
		<header>
			<nav>
				<div class="header">
					<img class="logo" src="@/assets/logo.png" alt="Logo Pong Ft_Transcendence">
					<h1 class="title">SETTINGS</h1>
				</div>
			</nav>
		</header>
		<main>
			<div class="settings-container">
        <div class="settings-group">
          <div class="volume-control">
            <input type="range" v-model="settings.volume" id="volume" min="0" max="100"/>
            <svg viewBox="0 0 200 50" class="wave-svg">
              <path :d="wavePath" fill="red" />
            </svg>
          </div>
          <span class="volume-meter">{{ settings.volume }}%</span>
        </div>
      </div>
		</main>
		<footer>
			<div class="footer">
				<img class="logo" src="@/assets/logo.png" alt="Logo Pong Ft_Transcendence">
			</div>
		</footer>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Définition des paramètres audio
const settings = ref({
  sound: true,
  volume: 50,
});

// Calcul de la forme de l'onde en fonction du volume
const wavePath = computed(() => {
  const volume = settings.value.volume;
  const amplitude = volume / 2; // Amplitude en fonction du volume
  const points = [];
  
  for (let i = 0; i <= 200; i += 5) {
    const y = 25 + amplitude * Math.sin((i / 20) * Math.PI);
    points.push(`${i},${y}`);
  }
  
  return `M ${points.join(' L')} Z`; // Crée le chemin SVG
});
</script>

<style scoped>

@import '../../styles/MainStyle.css';
@import '../../styles/SettingsStyle.css';

.settings-container {
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  margin: 20px auto;
}

.volume-control {
  display: flex;
  align-items: center;
}

.settings-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.settings-group input[type="range"] {
  width: 100%;
  margin-right: 100px; /* Espace entre le curseur et la vague */
	background: transparent;
}

/* Styles pour le curseur de volume */
.settings-group input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 10px; /* Largeur du curseur */
  height: 10px; /* Hauteur du curseur */
  background: hsl(0, 100%, 59%);
  border-radius: 50%; /* Forme ronde */
}

.settings-group input[type="range"]::-webkit-slider-runnable-track {
  height: 5px; /* Hauteur de la barre */
  background: hsl(0, 100%, 59%);
  border-radius: 5px; /* Coins arrondis */
}

/* Pour Firefox */
.settings-group input[type="range"]::-moz-range-thumb {
  width: 10px;
  height: 10px;
  background: hsl(0, 100%, 59%);
  border-radius: 50%;
}

.settings-group input[type="range"]::-moz-range-track {
  height: 5px;
  background: hsl(0, 100%, 59%);
  border-radius: 5px;
}

.wave-svg {
  width: 400px; /* Largeur du SVG pour la vague */
  height: 200px; /* Hauteur du SVG */
}
</style>