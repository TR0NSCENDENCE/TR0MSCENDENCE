<template>
	<router-link class="userviewer" v-bind:to="`/profile/${userdata.pk}`" target="_blank">
		<p id="username">{{ userdata.username + (store.getters.userId == userdata.pk ? ' (me)' : '') }}</p>
		<img class="user-pp" :src="userdata.user_profile.get_thumbnail" width="50"/>
	</router-link>
</template>

<script setup>
import store from '@store';

const props = defineProps([ 'userdata' ]);
</script>

<style scoped>
.user-pp {
	border-radius: 4px;
}

.userviewer {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
	padding: 0;
	text-decoration: none;
	color: var(--glow-color);
	cursor: pointer;
	border: 0.15em solid var(--glow-color);
	border-radius: 0.45em;
	padding: 1vh 2.5vh;
	letter-spacing: 0.2em;
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	animation: border-flicker 7s linear infinite;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
	width: fit-content;
}

#username {
	font-size: 1em;
	margin-right: 5%;
	white-space: nowrap;
}

@keyframes border-flicker {
	0% {
		opacity: 0.6;
	}

	10% {
		opacity: 0.9;
	}

	19% {
		opacity: 1;
	}

	31% {
		opacity: 0.7;
	}

	42% {
		opacity: 0.8;
	}

	61% {
		opacity: 0.5;
	}

	70% {
		opacity: 1;
	}

	100% {
		opacity: 0.9;
	}
}
</style>
