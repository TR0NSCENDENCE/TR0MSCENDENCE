import {defaults} from '@assets/game/pong/defaults.json'
import { Side } from './utils';

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

	#scores;
	#finished;
	#loser_id;

	constructor() {
		this.#timer = undefined;
		this.#scores = [0, -1];
		this.#finished = false;
		this.#loser_id = Side.ONE;
		this.#reset()
		this.onRestart = (loser_id) => {};
		this.#ball.position.x = defaults.scene.paddle_distance;
		this.#ball.position.y = defaults.scene.wall_distance;
	}

	#reset_ball = () => {
		let angle = defaults.ball.reset_angle_bounds;

		angle += Math.random() * defaults.ball.reset_angle_range;
		if (this.#loser_id === Side.TWO)
			angle += Math.PI;
		this.#ball.velocity.x = Math.cos(angle);
		this.#ball.velocity.y = Math.sin(angle);
	}

	#reset = () => {
		this.#ball = structuredClone(DEFAULT_SCENE_STATE.ball);
		this.#paddles = structuredClone(DEFAULT_SCENE_STATE.paddles);
		this.#reset_ball();
	}

	setBall = ({position, velocity, speed}) => {
		this.#ball.position = position;
		this.#ball.velocity = velocity;
		this.#ball.speed = speed;
	}

	setPaddle = (id, {position, speed}) => {
		console.assert(id === 0 || id ===1);
		this.#paddles[id].position.x = position.x;
		this.#paddles[id].position.y = position.y;
		this.#paddles[id].speed = speed
	}

	setLoser = (id) => {
		console.assert(id === 0 || id ===1);
		this.#loser_id = id;
		this.#scores[1 - id] += 1;
		this.#finished = this.#scores[1 - id] == defaults.game.win_score;
		this.#reset();
		this.onRestart(this.#loser_id);
	}

	forceUpdate = (state=DEFAULT_SCENE_STATE) => {
		this.setBall(state.ball);
		this.setPaddle(0, state.paddles[0]);
		this.setPaddle(1, state.paddles[1]);
		this.getElapsedTime();
	}

	getBall = () => {
		return ({
			position: this.#ball.position,
			velocity: this.#ball.velocity,
			speed: this.#ball.speed
		});
	}

	getPaddle = (id) => {
		console.assert(id === 0 || id === 1);
		const paddle = this.#paddles[id];
		return ({
			position: {
				x: paddle.position.x,
				y: paddle.position.y,
			},
			speed: paddle.speed
		});
	}

	getLoserId = () => this.#loser_id;
	isFinished = () => this.#finished;

	getScores = () => [ this.#scores[0], this.#scores[1] ];

	getElapsedTime = () => {
		if (this.#timer === undefined) {
			this.#timer = new Timer();
			this.#timer.start();
		}
		return (this.#timer.get_elapsed_time());
	}
}
