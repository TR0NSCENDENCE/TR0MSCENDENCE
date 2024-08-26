<template>
	<div id="friends-view">
		<div id="friends-container">
			<h1>Friends list</h1>
			<ul>
				<li v-for="friend in friends_list">
					<UserViewer style="margin-right: 2vw;" :userdata="friend"/>
					<GlowingButton style="font-size: 2vmin; width: 30vmin;padding: 0; height: 5vmin;" :text="'remove friend'" @click="removeFriend(friend.pk)"/>
				</li>
			</ul>
		</div>
		<div id="requests-container">
			<h1>Requests list</h1>
			<ul>
				<li v-for="request in requests_list">
					<UserViewer style="margin-right: 2vw;" :pk="request.from_user"/>
					<GlowingButton style="font-size: 2vmin; width: 18vmin;padding: 0; height: 5vmin;margin-right: 2vw;" :text="'accept'" @click="acceptRequest(request.id)"/>
					<GlowingButton style="font-size: 2vmin; width: 18vmin;padding: 0; height: 5vmin;" :text="'reject'" @click="rejectRequest(request.id)"/>
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup>
import GlowingButton from '@components/GlowingButton.vue';
import UserViewer from '@components/UserViewer.vue';
import { axiosInstance } from '@utils/api';
import { onMounted, ref } from 'vue';

const friends_list = ref('');
const friends_page = ref({
	next: null,
	prev: null,
	curpage: 0,
	totalpage: 0
});
const requests_list = ref([]);
const requests_page = ref({
	next: null,
	prev: null,
	curpage: 0,
	totalpage: 0
});

async function removeFriend(pk) {
	try {
		await axiosInstance.delete(`/user/${pk}/remove-friend/`);
		await updateFriendsList();
	} catch (e) {
		console.log(e);
	}
}

async function acceptRequest(id) {
	try {
		await axiosInstance.post(`/friend-request/${id}/accept/`);
		await updateFriendsList();
		await updateRequestsList();
	} catch (e) {
		console.log(e);
	}
}

async function rejectRequest(id) {
	try {
		await axiosInstance.delete(`/friend-request/${id}/reject/`);
		await updateRequestsList();
	} catch (e) {
		console.log(e);
	}
}

async function _updateFriendsList(url) {
	try {
		const response = await axiosInstance.get(url);
		const data = response.data;

		friends_list.value = data.results;
		friends_page.value.curpage = new URL(response.request.responseURL).searchParams.get('page') || 1;
		friends_page.value.totalpage = Math.ceil(data.count / 5);
		friends_page.value.next = data.next;
		friends_page.value.prev = data.prev;
	} catch (e) {
		console.log(e);
	}
}

async function updateFriendsList() {
	await _updateFriendsList('/user/friend-list/');
}

async function _updateRequestsList(url) {
	try {
		const response = await axiosInstance.get(url);
		const data = response.data;

		requests_list.value = data.results;
		requests_page.value.curpage = new URL(response.request.responseURL).searchParams.get('page') || 1;
		requests_page.value.totalpage = Math.ceil(data.count / 5);
		requests_page.value.next = data.next;
		requests_page.value.prev = data.prev;
	} catch (e) {
		console.log(e);
	}
}

async function updateRequestsList() {
	await _updateRequestsList('/user/friend-request-received/');
}

async function setup() {
	updateFriendsList();
	updateRequestsList();
}

onMounted(setup);

</script>

<style scoped>
#friends-view {
	display: flex;
	flex-direction: row;
}

#friends-container, #requests-container {
	width: 100%;
	padding-left: 4vw;
}

h1 {
	font-size: 4vmin;
	color: var(--glow-color);
	text-shadow: 0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em var(--glow-color);
}

ul {
	list-style-type: none;
	width: fit-content;
	font-size: 2vmin;
	padding-left: 2vw;
}

li {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	align-items: center;
}

</style>