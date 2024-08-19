<template>
	<div class="profile">
		<div class="profile-container">
			<div class="profile-info">
				<h2>Personal Information</h2>
				<p>Name - <span class="username">{{ userdata.username }}</span></p>
				<p>Email - <span class="email">{{ userdata.email }}</span></p>
			</div>
			<div id="profile-picture-container">
				<img id="profile-picture" :src="userdata.user_profile.get_thumbnail"/>
				<div v-if="store.getters.userId == pk">
					<input id="new-profile-picture" type="file" @change="onProfilePicturePicked" accept=".jpg" ref="file_picker" style="visibility:hidden"/>
					<GlowingButton @click="loadNewProfilePicture()" :text="'UPDATE PICTURE'"/>
				</div>
			</div>
		</div>
		<div class="profile-container">
			<div class="profile-stats">
				<h2>Statistics</h2>
				<ul>
					<li> Games Played - {{ winned + losed }} </li>
					<li> Games Won - {{ winned }} </li>
					<li> Win Rate - {{ winned + losed == 0 ? 0 : Math.round((winned / (winned + losed)) * 100) }}% </li>
				</ul>
			</div>
		</div>
		<div class="profile-activity">
			<h2>Last Games</h2>
			<ul>
				<li v-for="match in matchs">
					{{ match.player_one.username }} vs {{ match.player_two.username }} | {{ match.score }} - {{ match.opponent_score }} |
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup>
import { axiosInstance } from '@utils/api';
import { onMounted, ref } from 'vue';
import GlowingButton from './GlowingButton.vue';
import store from '@store';

const props = defineProps([ 'pk' ]);
// const win_rate = Math.round(100 * props.userdata.stats.wins / props.userdata.stats.played);

const userdata = ref({
	user_profile: {
		get_thumbnail: '',
	},
});
const winned = ref(0);
const losed = ref(0);
const matchs = ref('');
const file_picker = ref( );

function loadNewProfilePicture() {
	file_picker.value.click();
}

function onProfilePicturePicked(event) {
	console.log(event.target.files);
	const formData = new FormData();
	formData.append('profile_picture', event.target.files[0]);
	axiosInstance.patch(`/user/${props.pk}/update/`, formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	}).then(
		(response) => loadProfile()
	).catch(
		(error) => console.log(error.response.data)
	)
}

function loadProfile() {
	axiosInstance.get(`/user/${props.pk}/`).then(
		(response) => userdata.value = response.data
	);
	axiosInstance.get(`/user/${props.pk}/winned/`).then(
		(response) => winned.value = response.data.winned_count
	);
	axiosInstance.get(`/user/${props.pk}/losed/`).then(
		(response) => losed.value = response.data.losed_count
	);
	axiosInstance.get(`/user/${props.pk}/matchs/`).then(
		(response) => matchs.value = response.data
	);
}

onMounted(() => {
	loadProfile();
});

</script>

<style scoped>
.profile {
	color: var(--glow-color);
	--size-factor: (0.00188323 * 70vw);
	font-size: calc(8 * var(--size-factor));
}

#profile-picture-container {
	display: flex;
	flex-direction: column;
	align-items: end;
}

#profile-picture {
	border-radius: 1em;
	width: 50%;
}

#profile-picture-container > .glowing_button {
	margin-top: 20px;
}

h1 {
	display: flex;
	justify-content: center;
	align-items: center;
	text-align: center;
	margin-top: 30vh;
	letter-spacing: 0.3em;
	font-size: 5vh;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.username, .email {
	font-family: 'Orbitron';
}

.profile-container {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 20px;
	margin: 20px;
	padding: 20px;
	border: 0.2em solid var(--glow-color);
	border-radius: 0.45em;
	background: none;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.profile-photo .photo {
	width: 150px;
	height: 150px;
	border-radius: 50%;
	object-fit: cover;
	border: 0.2em solid var(--glow-color);
	box-shadow: 0px 0px 0.5em 0px var(--glow-color);
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
}

.profile-stats {
	flex: 1;
	margin: 20px;
	padding: 20px;
}

.profile-stats h2 {
	margin-bottom: 15px;
}

.profile-stats ul {
	list-style-type: none;
	padding: 0;
}

.profile-stats ul li,
.profile-activity ul li,
.profile-info p {
	margin-bottom: 10px;
}

.profile-activity {
	margin: 20px;
	padding: 20px;
	border: 0.2em solid var(--glow-color);
	border-radius: 0.45em;
	background: none;
	-webkit-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	-moz-box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	box-shadow: inset 0px 0px 0.5em 0px var(--glow-color),
		0px 0px 0.5em 0px var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

.profile-activity h2 {
	margin-left: 20px;
	padding: 20px;
}

.profile-activity ul {
	list-style-type: none;
}

.profile-activity li {
	margin-bottom: 5px;
}

.profile-info {
	margin: 20px;
	padding: 20px;
	background: none;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}
</style>
