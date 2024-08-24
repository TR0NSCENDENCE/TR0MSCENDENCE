const paddle_position = {
	x: 35,
	y: 0
}

export default class PongModel {
	#ball = {
		position: {
			x: 0,
			y: 0
		},
		velocity: {
			x: 0.0,
			y: 0.0
		}
	};

	#paddles = [
		{
			position: {
				x: -paddle_position.x,
				y: paddle_position.y
			}
		},
		{
			position: {
				x: paddle_position.x,
				y: paddle_position.y
			}
		},
	];

	setBall = (position, velocity) => {
		this.#ball.position.x = position.x;
		this.#ball.position.y = position.y;
		this.#ball.velocity.x = velocity.x;
		this.#ball.velocity.y = velocity.y;
	}

	setPaddle1 = (position) => {
		this.#paddles[0].position.x = position.x;
		this.#paddles[0].position.y = position.y;
	}

	setPaddle2 = (position) => {
		this.#paddles[1].position.x = position.x;
		this.#paddles[1].position.y = position.y;
	}

	getBall = () => {
		return ({
			position: this.#ball.position
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
}
