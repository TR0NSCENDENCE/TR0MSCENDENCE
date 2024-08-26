<template>
	<div id="register_page">
		<div class="form-container" v-on:keypress.enter="login" v-if="!otp">
			<div class="form-group">
				<label for="username">login:</label>
				<input type="text" id="username" ref="username"/>
			</div>
			<div class="form-group">
				<label for="password">password:</label>
				<input type="password" id="password" ref="password"/>
			</div>
			<div class="button-group">
				<GlowingButton class="small-button" :text="'login'" @click="login"/>
			</div>
		</div>
		<div id="opt-form" v-else>
			<p>A code of 4 digits was sent to your email</p>
			<div class="form-container" v-on:keypress.enter="checkOtp">
				<div class="form-group">
					<label for="otp_digit">otp digits ({{ otp_try }} try remaining):</label>
					<input type="text" id="otp_digit" ref="otp_digit"/>
				</div>
				<p v-if="bad_otp">Bad code</p>
				<div class="button-group">
					<GlowingButton class="small-button" :text="'validate'" @click="checkOtp"/>
				</div>
			</div>
		</div>
		<GlowingButton class="go-back-button small-button" :text="'go back home'" :dest="'/'"/>
		<p v-if="exists">Incorrect Username or Password, Try again</p>
	</div>
</template>

<script setup>
import GlowingButton from '@/components/GlowingButton.vue';
import { ref } from 'vue';
import store from '@store';
import router from '@router/index';
import { axiosInstance } from '@utils/api';

const username = ref(null);
const password = ref(null);
const exists = ref(false);
const otp_uuid = ref('');
const otp = ref(false);
const otp_digit = ref(null);
const otp_try = ref(0);
const bad_otp = ref(false);

async function checkOtp() {
	bad_otp.value = false;
	const payload = {
		otp: otp_digit.value.value,
	}
	try {
		const response = await axiosInstance.post(`/token/otp/${otp_uuid.value}/`, payload);
		store.dispatch('authentificate', response.data).then(
			() => router.push('/')
		);
	} catch (e) {
		if (e.response) {
			if (typeof e.response.data.remaining_tries !== 'undefined') {
				otp_try.value = e.response.data.remaining_tries;
			}
			if (e.response.status === 404) {
				otp.value = false;
			}
		}
		if (otp_try.value <= 0) {
			otp.value = false;
		}
		bad_otp.value = true;
	}
}

async function login() {
	exists.value = false;
	const payload = {
		username: username.value.value,
		password: password.value.value
	};
	try {
		const response = await axiosInstance.post('/login/', payload);
		otp_uuid.value = response.data.otp_uuid;
		otp.value = true;
		bad_otp.value = false;
		otp_try.value = 3;
	} catch (e) {
		exists.value = true;
	}
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

.form-group {
	margin-bottom: 2vh;
	width: 100%;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

#opt-form {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

#username, #password, #otp_digit {
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
	font-family: 'Orbitron', sans-serif;
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

.form-container {
	width: 50vh;
}

label {
	display: block;
	margin-bottom: 0.5vh;
	font-size: 2vh;
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

p {
	margin-top: 5vh;
	letter-spacing: 0.2em;
	text-align: center;
	font-size: 2vmin;
	font-weight: bolder;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}
</style>
