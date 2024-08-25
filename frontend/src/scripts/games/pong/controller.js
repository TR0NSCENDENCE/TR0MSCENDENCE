import PongModel, { DEFAULT_SCENE_STATE } from './model';
import { Direction } from './utils';

export default class PongController {
	#has_round_ended = true;
	#countdown_active = false;

	constructor() {
		this.onUpdateFinished = (state=DEFAULT_SCENE_STATE) => {};
		this.onCountdownStart = () => {};
		this.onCountdownStop = () => {};
		this.onPlayerOneInputRequested = () => Direction.NONE;
		this.onPlayerTwoInputRequested = () => Direction.NONE;
		this.onResetRequested = () => {};
		this.onBallRequested = () => DEFAULT_SCENE_STATE.ball;
		this.onPaddle1Requested = () => DEFAULT_SCENE_STATE.paddles[0];
		this.onPaddle2Requested = () => DEFAULT_SCENE_STATE.paddles[1];
		this.onBallUpdated = (ball) => {}
		this.onPaddle1Updated = (paddle) => {}
		this.onPaddle2Updated = (paddle) => {}
		this.onElapsedTimeRequested = () => 0;
	}

	#start_countdown = () => {
		this.#countdown_active = true;
		setTimeout(
			() => {
				this.#countdown_active = false
				this.onCountdownStop();
			},
			3000
		);
		this.onCountdownStart();
	}

	#reset = () => {
		this.onResetRequested();
		this.#start_countdown();
	}

	#simulation_step = (delta) => {
		const {position, velocity} = this.onBallRequested();
		position.x += 0.1
		this.onBallUpdated({position, velocity});
	}

	step = () => {
		if (this.#has_round_ended) {
			this.#has_round_ended = false;
			this.#reset()
		}
		if (!this.#countdown_active) {
			const delta = this.onElapsedTimeRequested();
			this.#simulation_step(delta);
		}
		this.onUpdateFinished();
	}
}
