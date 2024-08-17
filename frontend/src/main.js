import { createApp } from 'vue';

import App from '@/App.vue';
import router from '@router';
import store from '@store';

import '@assets/default.css';

createApp(App)
	.use(router)
	.use(store)
	.mount('#app');
