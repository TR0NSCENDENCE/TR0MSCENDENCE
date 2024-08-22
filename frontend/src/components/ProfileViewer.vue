<template>
	<div class="profile">
		<div class="profile-container">
			<div class="profile-info">
				<h2>Personal Information</h2>
				<p>Name - <span class="username">{{ userdata.username }}</span></p>
				<div v-if="store.getters.userId == pk">
					<input type="text" id="new_username" ref="new_username"/>
					<p>{{ error_txt.username }}</p>
					<GlowingButton class="fit-content" @click="newUsername()" :text="'update username'"/>
				</div>
				<p>Email - <span class="email">{{ userdata.email }}</span></p>
				<div v-if="store.getters.userId == pk">
					<input type="email" id="new_email" ref="new_email"/>
					<p>{{ error_txt.email }}</p>
					<GlowingButton class="fit-content" @click="newEmail()" :text="'update email'"/>
				</div>
			</div>
			<div id="profile-picture-container">
				<img id="profile-picture" :src="userdata.user_profile.get_thumbnail"/>
				<div v-if="store.getters.userId == pk">
					<input id="new-profile-picture" type="file" @change="onProfilePicturePicked" accept=".jpg" ref="file_picker" style="visibility:hidden"/>
					<GlowingButton class="fit-content" @click="loadNewProfilePicture()" :text="'UPDATE PICTURE'"/>
				</div>
			</div>
		</div>
		<div class="profile-container" v-if="store.getters.isAuthenticated">
			<div class="profile-stats">
				<h2>Statistics</h2>
				<ul>
					<li> Games Played - {{ winned + losed }} </li>
					<li> Games Won - {{ winned }} </li>
					<li> Win Rate - {{ winned + losed == 0 ? 0 : Math.round((winned / (winned + losed)) * 100) }}% </li>
				</ul>
			</div>
		</div>
		<div class="profile-matchs" v-if="store.getters.isAuthenticated">
			<h2>Last Games</h2>
			<div id="matchs-list-pages">
				<ul>
					<li v-for="match in matchs">
						<MatchViewer :data="match"/>
					</li>
				</ul>
				<div id="nav-pages">
					<GlowingButton v-if="prev" @click="_updateMatchsList(prev)" :text="'previous'"/>
					<h2 v-if="prev || next" >page {{ curpage }}/{{ totalpage }}</h2>
					<GlowingButton v-if="next" @click="_updateMatchsList(next)" :text="'next'"/>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { axiosInstance } from '@utils/api';
import { onMounted, ref } from 'vue';
import GlowingButton from './GlowingButton.vue';
import store from '@store';
import MatchViewer from './MatchViewer.vue';

const props = defineProps([ 'pk' ]);
// const win_rate = Math.round(100 * props.userdata.stats.wins / props.userdata.stats.played);

const error_txt = ref({
	email: '',
	username: '',
});

function handleError(err) {
	for (var prop in error_txt.value)
		error_txt.value[prop] = (err.response.data[prop] ?? '')[0] ?? '';
}

const userdata = ref({
	user_profile: {
		get_thumbnail: '',
	},
});
const new_email = ref(null);
const new_username = ref(null);
const winned = ref(0);
const losed = ref(0);
const matchs = ref('');
const file_picker = ref();
const next = ref(null);
const prev = ref(null);
const curpage = ref(0);
const totalpage = ref(0);

function loadNewProfilePicture() {
	file_picker.value.click();
}

function _updateMatchsList(url) {
	axiosInstance.get(url).then(
		(response) => {
			curpage.value = new URL(response.request.responseURL).searchParams.get('page') || 1
			totalpage.value = Math.ceil(response.data.count / 5);
			next.value = response.data.next;
			prev.value = response.data.previous
			matchs.value = response.data.results;
		}
	);
}

function updateMatchsList() {
	_updateMatchsList(`/user/${props.pk}/matchs`);
}

function newUsername() {
	error_txt.value.username = '';
	axiosInstance.patch(`/user/${props.pk}/update-cred/`, {
		username: new_username.value.value
	}).then(
		(response) => loadProfile()
	).catch(handleError)
}

function newEmail() {
	error_txt.value.email = '';
	axiosInstance.patch(`/user/${props.pk}/update-cred/`, {
		email: new_email.value.value
	}).then(
		(response) => loadProfile()
	).catch(handleError)
}

function onProfilePicturePicked(event) {
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
	if (store.getters.isAuthenticated) {
		axiosInstance.get(`/user/${props.pk}/winned/`).then(
			(response) => winned.value = response.data.winned_count
		);
		axiosInstance.get(`/user/${props.pk}/losed/`).then(
			(response) => losed.value = response.data.losed_count
		);
		updateMatchsList();
	}
}

onMounted(() => {
	loadProfile();
});

</script>

<style scoped>
#matchs-list-pages {
	display: flex;
	justify-content: space-between;
}

#nav-pages {
	margin-left: 1vw;
	display: flex;
	flex-direction: column;
	align-items: center;
}

#new_username, #new_email {
	margin-bottom: 4px;
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

.fit-content {
	width: fit-content;
	height: fit-content;
	font-size: 1vmax;
}

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

#matchs-list-pages > li {
	width: fit-content;
}

#matchs-list-pages > ul {
	width: fit-content;
	margin: 0px;
}
.profile-stats ul li,
#matchs-list-pages ul li,
.profile-info p {
	margin-bottom: 10px;
}

.profile-matchs {
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

.profile-matchs h2 {
	margin-left: 20px;
	padding: 20px;
}

.profile-matchs ul {
	list-style-type: none;
}

.profile-matchs li {
	margin-bottom: 5px;
}

.profile-info {
	margin: 20px;
	padding: 20px;
	background: none;
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}
</style>
