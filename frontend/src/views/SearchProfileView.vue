<template>
	<div id="search-profile-view">
		<div id="search-bar">
			<input type="text" id="search-username" ref="search_username" @change="updateUserList"/>
		</div>
		<div id="result-list">
			<ul>
				<li v-for="user in users">
					<UserViewer :userdata="user"/>
				</li>
			</ul>
			<div id="nav-pages">
				<GlowingButton v-if="prev" @click="_updateUserList(prev)" :text="'previous'"/>
				<h1 v-if="prev || next" >page {{ curpage }}/{{ totalpage }}</h1>
				<GlowingButton v-if="next" @click="_updateUserList(next)" :text="'next'"/>
			</div>
		</div>
	</div>
</template>

<script setup>
import GlowingButton from '@components/GlowingButton.vue';
import UserViewer from '@components/UserViewer.vue';
import { axiosInstance } from '@utils/api';
import { onMounted, ref } from 'vue';


const search_username = ref(null);

const users = ref([]);
const next = ref(null);
const prev = ref(null);
const curpage = ref(0);
const totalpage = ref(0);

function _updateUserList(url) {
	axiosInstance.get(url).then(
		(response) => {
			curpage.value = new URL(response.request.responseURL).searchParams.get('page') || 1
			totalpage.value = Math.ceil(response.data.count / 5);
			next.value = response.data.next;
			prev.value = response.data.previous
			users.value = response.data.results;
		}
	);
}

function updateUserList() {
	const search = search_username.value.value;
	_updateUserList(`/user/search/?search=${search}`);
}

onMounted(updateUserList);

</script>

<style scoped>
#nav-pages {
	display: flex;
	justify-content:space-around;
	align-items: center;
	margin: 4%;
}

#search-profile-view {
	display: flex;
	flex-direction: column;
}

h1 {
	font-size: 100%;
	color: var(--glow-color);
}

ul {
	list-style-type: none;
	padding: 0;
}

li {
	margin: 5px;
}

#search-bar {
	display: flex;
	justify-content: center;
}

#search-username {
	width: 50vw;
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
	font-family: 'Orbitron', sans-serif;
	outline: none;
}
</style>
