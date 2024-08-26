import { Direction } from "@scripts/games/pong/utils";

export default {
	namespaced: true,
	state: {
		players: [
			Direction.NONE,
			Direction.NONE,
		]
	},
	mutations: {
		set_player_direction: (state, {id, direction}) => {
			console.assert(id === 0 || id === 1, `store pong invalid id ${id}`);
			state.players[id] = direction;
		},
		reset: (state) => {
			state.players[0] = Direction.NONE;
			state.players[1] = Direction.NONE;
		}
	},
	actions: {},
	getters: {
		player_direction: (state) => (id) => (state.players[id]),
	},
};
