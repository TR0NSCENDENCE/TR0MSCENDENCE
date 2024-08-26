import { createApp } from 'vue';

import App from '@/App.vue';
import router from '@router';
import store from '@store';

import '@assets/default.css';
import { setupInstance } from '@utils/api';

setupInstance();

store.dispatch('updateProfile');

createApp(App)
	.use(router)
	.use(store)
	.mount('#app');
