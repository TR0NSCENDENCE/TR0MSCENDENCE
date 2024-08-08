<template>
	<div class="logo-container">
	  <img class="logo" src="@assets/tr0nscendence_logo.webp" alt="Logo Pong Ft_Transcendence">
	</div>
  </template>
  

<style scoped>

.logo-container {
  width: 8vh;
  height: 8vh;
  border-radius: 50%;
  overflow: hidden;
  margin: 10px;
  -webkit-box-shadow: inset 0px 0px 1.75em 0px var(--glow-color), 0px 0px 1.75vh 0px var(--glow-color);
  -moz-box-shadow: inset 0px 0px 1.75em 0px var(--glow-color), 0px 0px 1.75vh 0px var(--glow-color);
  box-shadow: inset 0px 0px 1.75em 0px var(--glow-color), 0px 0px 1.75vh 0px var(--glow-color);
  border: 0.25vh solid var(--glow-color);
  perspective: 2em;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo {
  width: 100%;
  height: 100%;
  filter: var(--logo-filter);
}
</style>