<template>
	<div id="register_page">
		<div v-on:keypress.enter="register" v-if="!success">
			<form @submit.prevent="submitForm">
				<div class="form-group">
					<div class="label-error-group">
						<label for="email">email:</label>
						<p class="error-detail">{{ error_txt.email }}</p>
					</div>
					<input type="email" id="email" ref="email">
				</div>
				<div class="form-group">
					<div class="label-error-group">
						<label for="username">login:</label>
						<p class="error-detail">{{ error_txt.username }}</p>
					</div>
					<input type="text" id="username" ref="username">
				</div>
				<div class="form-group">
					<div class="label-error-group">
						<label for="password">password:</label>
						<p class="error-detail">{{ error_txt.password }}</p>
					</div>
					<input type="password" id="password" ref="password">
				</div>
				<div class="form-group">
					<div class="label-error-group">
						<label for="repassword">retype password:</label>
						<p class="error-detail">{{ error_txt.repassword }}</p>
					</div>
					<input type="password" id="repassword" ref="repassword">
				</div>
				<div class="button-group">
					<GlowingButton class="small-button" :type="'submit'" :text="'register'" @click="register" />
				</div>
			</form>
		</div>
		<div v-else>
			<h1>
				Your account was successfuly created<br>You need to activate it, check your mails ({{ register_email }})
			</h1>
		</div>
		<GlowingButton class="go-back-button small-button" :text="'go back home'" :dest="'/'" />
	</div>
</template>

<script setup>
import GlowingButton from '@/components/GlowingButton.vue'
import { ref } from 'vue';
import router from '@router/index';
import store from '@store';
import { axiosInstance } from '@utils/api';

const email = ref(null);
const register_email = ref('');
const username = ref(null);
const password = ref(null);
const repassword = ref(null);
const success = ref(false);

const error_txt = ref({
	email: '',
	username: '',
	password: '',
	repassword: '',
});

// TODO: Do the error handling.
async function register() {
	const payload = {
		email: email.value.value,
		username: username.value.value,
		password: password.value.value,
		repassword: repassword.value.value,
	};
	axiosInstance.post('/register/', payload).then(
		async (response) => {
			success.value = true;
			register_email.value = payload.email;
		}
	).catch(
		(error) => {
			if (!error.response)
				return ;
			for (var prop in error_txt.value)
				error_txt.value[prop] = (error.response.data[prop] ?? '')[0] ?? '';
		}
	);
}
</script>

<style scoped>
#register_page {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	color: var(--glow-color);
	font-size: 3vmin;
}

h1 {
	font-size: 2vmin;
	text-align: center;
}

#email, #username {
	font-family: 'Orbitron';
}

.form-group, h1 {
	margin-bottom: 2vh;
	width: 100%;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.label-error-group {
	display: flex;
	flex-direction: row;
	width: fit-content;
}

.form-group>input {
	width: 100%;
	padding: 1vh;
	background-color: black;
	border: 0.15em solid var(--glow-color);
	border-radius: 0.45em;
	color: var(--glow-color);
	box-sizing: border-box;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	animation: border-flicker 7s linear infinite;
	font-family: 'SpaceTron', sans-serif;
	outline: none;
}

.button-group {
	display: flex;
	justify-content: space-between;
	width: 100%;
	margin-top: 2vh;
}

.button-group .small-button {
	margin-right: 1vh;
	flex: 1;
}

.button-group .small-button:last-child {
	margin-right: 0;
}

form {
	width: 50vh;
}

.error-detail {
	font-size: x-small;
}

label,
.error-detail {
	display: block;
	margin: 0.5vh;
}

.small-button {
	padding: 1vh 2vh;
	font-size: 0.8em;
	min-width: 12vh;
}

.go-back-button {
	margin-top: 2vh;
	width: 45.7vh;
}
</style>
