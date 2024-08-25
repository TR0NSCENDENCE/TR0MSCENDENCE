const PADDLE_DISTANCE = 35;

export const DEFAULT_SCENE_STATE = Object.freeze({
	ball: {
		position: {
			x: 0,
			y: 0
		},
		velocity: {
			x: 0,
			y: 0
		}
	},
	paddles: [
		{
			position: {
				x: -PADDLE_DISTANCE,
				y: 0
			}
		},
		{
			position: {
				x: PADDLE_DISTANCE,
				y: 0
			}
		}
	]
})

class Timer {
	#time = undefined;

	#get_time = () =>new Date().getTime(); 

	start = () => {
		this.#time = this.#get_time();
	}

	get_elapsed_time = () => {
		const now = this.#get_time();
		const elapsed_time = (now - this.#time) / 1000.;

		this.#time = now;
		return (elapsed_time);
	}
}

export default class PongModel {
	#ball;
	#paddles;
	#timer;

	constructor() {
		this.#timer = undefined;
		this.reset()
	}

	reset = () => {
		console.log('model "reset"');
		this.#ball = structuredClone(DEFAULT_SCENE_STATE.ball);
		this.#paddles = structuredClone(DEFAULT_SCENE_STATE.paddles);
	}

	setBall = (position, velocity) => {
		console.log('model "setBall"');
		this.#ball.position = position;
		this.#ball.velocity = velocity;
	}

	setPaddle1 = (position) => {
		console.log('model "setPaddle1"');
		this.#paddles[0].position = position;
	}

	setPaddle2 = (position) => {
		console.log('model "setPaddle2"');
		this.#paddles[1].position = position;
	}

	forceUpdate = (state=DEFAULT_SCENE_STATE) => {
		console.log('model "forceUpdate"');
		this.setBall(state.ball.position, state.ball.velocity);
		this.setPaddle1(state.paddles[0].position);
		this.setPaddle2(state.paddles[1].position);
		this.getElapsedTime();
	}

	getBall = () => {
		return ({
			position: this.#ball.position,
			velocity: this.#ball.velocity
		});
	}

	getPaddle1 = () => {
		return ({
			position: this.#paddles[0].position
		});
	}

	getPaddle2 = () => {
		return ({
			position: this.#paddles[1].position
		});
	}

	getElapsedTime = () => {
		if (this.#timer === undefined) {
			this.#timer = new Timer();
			this.#timer.start();
		}
		return (this.#timer.get_elapsed_time());
	}
}
