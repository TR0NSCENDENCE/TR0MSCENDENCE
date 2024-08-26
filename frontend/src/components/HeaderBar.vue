<template>
	<nav class="header">
		<router-link to="/">
			<TranscendenceLogo />
		</router-link>
		<div class="sub-header">
			<div v-if="store.getters.isAuthenticated" class="sub-header-link">
				<div class="signIn-link" @click="logout">
					<h1 class="header-box signIn">
						logout
					</h1>
				</div>
				<div class="signIn-link" @click="router.push('/profile')">
					<h1 class="header-box signIn">
						my profile ({{ store.getters.authUser }})
					</h1>
				</div>
			</div>
			<div v-else class="sub-header-link">
				<router-link to="/login" class="signIn-link">
					<h1 class="header-box signIn">login</h1>
				</router-link>
				<router-link to="/register" class="signIn-link">
					<h1 class="header-box signIn">register</h1>
				</router-link>
			</div>
			<div class="transcendence-title">
				<h1 class="header-box title">{{ title }}</h1>
			</div>
		</div>
	</nav>
</template>

<script setup>
import TranscendenceLogo from '@components/TranscendenceLogo.vue';
import { ref, onMounted, onUnmounted } from 'vue'
import store from '@store';
import router from '@router/index';

let mutation_observer;
const title = ref(0);

function updateTitle() {
	title.value = document.title
}

async function logout() {
	store.dispatch('deauthentificate');
	router.push('/');
}

onMounted(() => {
	mutation_observer = new MutationObserver(updateTitle);
	mutation_observer.observe(
		document.querySelector('title'),
		{ subtree: true, characterData: true, childList: true }
	)
	updateTitle();
});

onUnmounted(() => {
	mutation_observer.disconnect();
	mutation_observer = undefined;
});
</script>

<style scoped>
h1 {
	margin: 1vmin;
}

.header {
	display: flex;
	flex-direction: row;
	align-items: center;
	text-align: center;
	height: fit-content;
	width: 100%;
}

.transcendence-title {
	flex: 1 1 0;
}

.sub-header {
	flex: 1 1 0;
	display: flex;
	font-size: 1vw;
}

.sub-header-link {
	display: flex;
	justify-content: space-between;
	width: fit-content;
}

.header-box {
	color: var(--glow-color);
	padding: 0.35em 1em;
	border: 0.15em solid var(--glow-color);
	border-radius: 0.45em;
	background: none;
	white-space: nowrap;
	perspective: 1em;
	font-family: "SpaceTron", sans-serif;
	font-weight: 900;
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

.signIn-link {
	text-decoration: none;
	cursor: pointer;
}

.signIn::after {
	content: "";
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	opacity: 0;
	z-index: -1;
	color: rgba(0, 0, 0, 0.8);
	background-color: var(--glow-color);
	box-shadow: 0 0 2em 0.2em var(--glow-color);
	transition: opacity 100ms linear;
}

.signIn:hover {
	color: rgba(0, 0, 0, 0.8);
	text-shadow: none;
	animation: none;
}

.signIn {
	flex: 1 0 40%;
	text-align: center;
	margin-right: 1vw;
	margin-left: 1vw;
	letter-spacing: 0.1em;
}

.signIn:hover:before {
	filter: blur(1.5em);
	opacity: 1;
}

.signIn:hover:after {
	opacity: 1;
}

.title {
	text-align: right;
	letter-spacing: 0.6em;
}
</style>
