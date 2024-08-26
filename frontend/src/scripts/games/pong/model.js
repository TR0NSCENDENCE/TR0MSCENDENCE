import {defaults} from '@assets/game/pong/defaults.json'

export const DEFAULT_SCENE_STATE = Object.freeze({
	ball: {
		position: {
			x: 0,
			y: 0
		},
		velocity: {
			x: 0,
			y: 0
		},
		speed: defaults.ball.velocity
	},
	paddles: [
		{
			position: {
				x: defaults.scene.paddle_distance,
				y: 0
			},
			speed: defaults.paddle.velocity
		},
		{
			position: {
				x: -defaults.scene.paddle_distance,
				y: 0
			},
			speed: defaults.paddle.velocity
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
		this.#ball = structuredClone(DEFAULT_SCENE_STATE.ball);
		this.#paddles = structuredClone(DEFAULT_SCENE_STATE.paddles);
	}

	setBall = ({position, velocity, speed}) => {
		this.#ball.position = position;
		this.#ball.velocity = velocity;
		this.#ball.speed = speed;
	}

	setPaddle1 = ({position, speed}) => {
		this.#paddles[0].position = position;
		this.#paddles[0].speed = speed
	}

	setPaddle2 = ({position, speed}) => {
		this.#paddles[1].position = position;
		this.#paddles[1].speed = speed
	}

	forceUpdate = (state=DEFAULT_SCENE_STATE) => {
		this.setBall(state.ball);
		this.setPaddle1(state.paddles[0]);
		this.setPaddle2(state.paddles[1]);
		this.getElapsedTime();
	}

	getBall = () => {
		return ({
			position: this.#ball.position,
			velocity: this.#ball.velocity,
			speed: this.#ball.speed
		});
	}

	getPaddle1 = () => {
		return ({
			position: this.#paddles[0].position,
			speed: this.#paddles[0].speed
		});
	}

	getPaddle2 = () => {
		return ({
			position: this.#paddles[1].position,
			speed: this.#paddles[1].speed
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
