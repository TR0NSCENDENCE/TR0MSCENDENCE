const paddle_position = {
	x: 35,
	y: 0
}

export default class PongLogic {
	#ball = {
		position: {
			x: 0,
			y: 0
		},
		velocity: {
			x: 0.5,
			y: 0.5
		}
	};

	#paddle_1 = {
		position: {
			x: -paddle_position.x,
			y: paddle_position.y
		}
	};

	#paddle_2 = {
		position: {
			x: paddle_position.x,
			y: paddle_position.y
		}
	};

	#callbacks;

	constructor(
		callbacks={
			onUpdateFinished: (
				ball={
					position: {x: 0, y: 0}
				},
				paddle1={
					position: {x: 0, y: 0}
				},
				paddle2={
					position: {x: 0, y: 0}
				}
			) => {}
		}
	) {
		this.#callbacks = callbacks;
	}

	step = () => {
		this.#callbacks.onUpdateFinished(
			this.getBall(),
			this.getPaddle1(),
			this.getPaddle2()
		);
	}

	setBall = (position, velocity) => {
		this.#ball.position.x = position.x;
		this.#ball.position.y = position.y;
		this.#ball.velocity.x = velocity.x;
		this.#ball.velocity.y = velocity.y;
	}

	setPaddle1 = (position) => {
		this.#paddle_1.position.x = position.x;
		this.#paddle_1.position.y = position.y;
	}

	setPaddle2 = (position) => {
		this.#paddle_2.position.x = position.x;
		this.#paddle_2.position.y = position.y;
	}

	getBall = () => {
		return ({
			position: this.#ball.position
		});
	}

	getPaddle1 = () => {
		return ({
			position: this.#paddle_1.position
		});
	}

	getPaddle2 = () => {
		return ({
			position: this.#paddle_2.position
		});
	}

	setCallbackUpdateFinished = (onUpdateFinished) => {
		this.#callbacks.onUpdateFinished = onUpdateFinished;
	}
}
