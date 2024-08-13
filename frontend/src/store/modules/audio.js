export default {
	namespaced: true,
	state: {
		currentTrack: null,
		volume: 1.0,
		isPlaying: false,
	},
	mutations: {
		set_track(state, track) {
			state.currentTrack = track;
		},
		set_volume(state, volume) {
			state.volume = volume;
		},
		set_playing(state, isPlaying) {
			state.isPlaying = isPlaying;
		},
	},
	actions: {
		playMusic({ commit }, track) {
			commit('set_track', track);
			commit('set_playing', true);
		},
		setVolume({ commit }, volume) {
			commit('set_volume', volume);
		},
		stopMusic({ commit }) {
			commit('set_playing', false);
		},
	},
	getters: {
		currentTrack: (state) => state.currentTrack,
		volume: (state) => state.volume,
		isPlaying: (state) => state.isPlaying,
	},
};
