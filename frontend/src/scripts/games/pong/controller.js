import store from '@store';
import PongModel, { DEFAULT_SCENE_STATE } from './model';
import PongRenderer from './renderer';
import { Direction } from './utils';
import { defaults } from '@assets/game/pong/defaults.json'

defaults.paddle.max_position = defaults.scene.wall_distance - defaults.paddle.size / 2.
defaults.ball.reset_angle_bounds = Math.atan2(defaults.scene.paddle_distance, defaults.scene.wall_distance);
defaults.ball.reset_angle_range = 2. * defaults.ball.reset_angle_bounds - Math.PI

export default class PongController {
	/** @type {PongModel} */
	#model;
	/** @type {PongRenderer} */
	#renderer;
	#countdown_active;
	#simulation_enabled;

	constructor(
		/** @type {PongModel} */ model,
		/** @type {PongRenderer} */ renderer,
		/** @type {boolean} */ enable_simulation=true
	) {
		this.#model = model;
		this.#renderer = renderer;
		this.#simulation_enabled = enable_simulation;
		this.onUpdateRequested = () => {};
		this.onCountdownStart = () => {};
		this.onCountdownStop = () => {};
		this.onPlayerOneInputRequested = () => Direction.NONE;
		this.onPlayerTwoInputRequested = () => Direction.NONE;
		this.onResetRequested = () => {};
		this.#model.onRestart = this.#start_round;
		this.#countdown_active = false;
	}

	#start_countdown = () => {
		this.#countdown_active = true;
		setTimeout(
			() => {
				this.#model.getElapsedTime();
				this.#countdown_active = false
				this.onCountdownStop();
			},
			3000
		);
		this.onCountdownStart();
	}

	#start_round = () => {
		this.#start_countdown();
	}

	#update_paddle = (delta, id) => {
		const can_move = (position) => {
			const half_padd = defaults.paddle.size / 2.;
			const limit = defaults.scene.wall_distance - half_padd;
			return (Math.abs(position) <= limit);
		}

		const direction = store.getters['pong/player_direction'](id);
		const {position, speed} = this.#model.getPaddle(id);

		position.y -= direction * speed * delta;
		if (!can_move(position.y))
			position.y = Math.sign(position.y) * defaults.paddle.max_position;
		this.#model.setPaddle(id, {position, speed});
	}

	#ball_update_position = (ball, step) => {
		ball.position.x += ball.velocity.x * step;
		ball.position.y += ball.velocity.y * step;
	}

	#ball_wall_collision = (ball) => {
		const bounds = defaults.scene.wall_distance - defaults.ball.radius;

		if (Math.abs(ball.position.y) < bounds)
			return;
		ball.position.y = Math.sign(ball.position.y) * (2 * bounds - Math.abs(ball.position.y));
		ball.velocity.y = -ball.velocity.y
	}

	#update_ball = (delta, onLose) => {
		let ball = this.#model.getBall();
		let remaining_distance = ball.speed * delta;

		while (remaining_distance > 0) {
			let step = Math.min(remaining_distance, 1);
			remaining_distance -= step;
			this.#ball_update_position(ball, step);
			this.#ball_wall_collision(ball);
			const loser_id = this.#paddle_collision();
			if (loser_id !== undefined) {
				onLose(loser_id);
				remaining_distance = 0;
			}
		}
	}

	#paddle_physics = (ball, id) => {
		const collides = (position, paddle) => {
			const delta = Math.abs(paddle - position)
			return (delta <= defaults.paddle.size / 2.);
		}

		const {position, speed} = this.#model.getPaddle(id);

		if (!collides(ball.position.y, position.y))
			return (true);

		let new_position = defaults.scene.paddle_distance;
		new_position -= defaults.ball.radius;
		ball.position.x = Math.sign(ball.position.x) * new_position;

		let angle = Math.atan2(defaults.paddle.size / 2., position.y - ball.position.y);
		angle -= Math.PI / 2.;
		if (position.x > 0)
			angle = Math.PI - angle;

		ball.speed *= defaults.ball.speedup_factor;
		ball.velocity.x = Math.cos(angle);
		ball.velocity.y = Math.sin(angle);

		this.#model.setPaddle(id, {position, speed: speed * defaults.paddle.speedup_factor});
		this.#model.setBall(ball);

		return (false);
	}

	#paddle_collision = () => {
		const ball = this.#model.getBall();

		if (Math.abs(ball.position.x) < defaults.scene.paddle_distance - defaults.ball.radius)
			return (undefined);
		const player_id = ball.position.x > 0 ? 0 : 1;
		return (this.#paddle_physics(ball, player_id) ? player_id : undefined);
	}

	#handle_physics = (delta) => {
		this.#update_paddle(delta, 0);
		this.#update_paddle(delta, 1);
		this.#update_ball(delta, this.#model.setLoser);
	}

	#render = () => {
		const state = {
			ball: this.#model.getBall(),
			paddles: [
				this.#model.getPaddle(0),
				this.#model.getPaddle(1)
			]
		};
		this.#renderer.updateState(state);
		this.#renderer.render();
	}

	step = () => {
		this.onUpdateRequested();
		if (this.#simulation_enabled && !this.#countdown_active) {
			const delta = this.#model.getElapsedTime();
			this.#handle_physics(delta);
		}
		this.#render()
	}
}
